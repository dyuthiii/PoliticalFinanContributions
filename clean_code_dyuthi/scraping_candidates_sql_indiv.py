# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 13:56:45 2024

@author: spark
"""

import requests
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime
import time
import pandas as pd
# Load environment variables
load_dotenv()

# def create_database(db_path='C:/Users/spark/OneDrive/Desktop/Poli_bot/Poli_bot_DB_final.db'):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()

#     # Drop tables if they exist to avoid schema mismatch
#     cursor.execute('DROP TABLE IF EXISTS contributions')
#     cursor.execute('DROP TABLE IF EXISTS candidates')

#     # Create candidates table
#     cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
#         candidate_id TEXT PRIMARY KEY,
#         name TEXT,
#         office TEXT,
#         party TEXT,
#         district TEXT,
#         active_through INTEGER
#     )''')

#     # Create contributions table with correct column names
#     cursor.execute('''CREATE TABLE IF NOT EXISTS contributions (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         candidate_id TEXT,
#         contribution_receipt_date TEXT,
#         contributor_name TEXT,
#         amount REAL,
#         contributor_city TEXT,
#         contributor_state TEXT,
#         contribution_type TEXT,
#         FOREIGN KEY(candidate_id) REFERENCES candidates(candidate_id)
#     )''')

#     conn.commit()
#     conn.close()

def search_candidate(api_key, candidate_name):
    base_url = "https://api.open.fec.gov/v1/candidates/search/"
    params = {
        "api_key": api_key,
        "q": candidate_name,
        "sort": "name"
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Debug output
        print(f"API Response: {data}")  # Log the API response
        
        results = data.get('results', [])
        
        if results:
            # Improved matching logic
            first_name, last_name = candidate_name.split()
            for r in results:
                api_name = r.get('name')
                if api_name:
                    api_last, api_first = api_name.split(", ")
                    if api_first.lower() == first_name.lower() and api_last.lower() == last_name.lower():
                        return r
        
        return None
    
    except requests.RequestException as e:
        print(f"Error searching for candidate: {e}")
        return None

def fetch_contributions(api_key, candidate_id, start_date, end_date):
    base_url = "https://api.open.fec.gov/v1/schedules/schedule_a/"
    start_date = datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    
    all_contributions = []
    page = 1

    # Determine the two-year transaction period based on the provided start and end dates
    start_year = int(start_date.split('-')[0])
    two_year_transaction_period = start_year if start_year % 2 == 0 else start_year - 1
    
    while True:
        params = {
            "api_key": api_key,
            "candidate_id": candidate_id,
            "min_date": start_date,
            "max_date": end_date,
            "per_page": 100,
            "sort": "-contribution_receipt_date",
            "page": page,
            "two_year_transaction_period": two_year_transaction_period
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            contributions = data.get('results', [])
            
            if not contributions:
                break
            
            all_contributions.extend(contributions)
            page += 1
            
            time.sleep(1)  # Respect rate limits
            
        except requests.RequestException as e:
            print(f"Error fetching contributions: {e}")
            break
    
    print(f"Fetched {len(all_contributions)} contributions for candidate ID {candidate_id}")
    return all_contributions

def store_candidate_in_sqlite(db_path, candidate_info):
    """
    Store candidate information in SQLite database
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''INSERT OR IGNORE INTO candidates (candidate_id, name, office, party, district, active_through)
                      VALUES (?, ?, ?, ?, ?, ?)''', (
        candidate_info['candidate_id'],
        candidate_info['name'],
        candidate_info.get('office_full', ''),
        candidate_info.get('party_full', ''),
        candidate_info.get('district', ''),
        candidate_info.get('active_through', 0)
    ))
    
    conn.commit()
    conn.close()

def store_contributions_in_sqlite(db_path, candidate_id, contributions):
    """
    Store contributions in SQLite database
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for contribution in contributions:
        cursor.execute('''INSERT INTO contributions (candidate_id, contribution_receipt_date, contributor_name, amount, contributor_city, contributor_state, contribution_type)
                          VALUES (?, ?, ?, ?, ?, ?, ?)''', (
            candidate_id,
            contribution.get('contribution_receipt_date', 'Unknown'),
            contribution.get('contributor_name', 'Unknown'),
            contribution.get('contribution_receipt_amount', 0),  # Make sure this key exists in the API response
            contribution.get('contributor_city', 'Unknown'),
            contribution.get('contributor_state', 'Unknown'),
            contribution.get('report_type', 'Unknown')
        ))
    
    conn.commit()
    conn.close()
    
    print(f"Stored {len(contributions)} contributions in database for candidate ID {candidate_id}")

def main():
    api_key = os.getenv("FEC_API_KEY")
    if not api_key:
        print("Error: FEC API key not found in environment variables.")
        return
    db_path = 'C:/Users/spark/OneDrive/Desktop/Poli_bot/Poli_bot_DB_final.db'
    #create_database(db_path)
    
    candidates = ["Connie Conway"]  # Ensure candidate names are accurate
    start_date = "01/01/2023"  # Adjust date range based on cycles
    end_date = "11/11/2024"
    
    for candidate_name in candidates:
        print(f"\nProcessing {candidate_name}")
        
        candidate_info = search_candidate(api_key, candidate_name)
        
        if candidate_info:
            candidate_id = candidate_info['candidate_id']
            store_candidate_in_sqlite(db_path, candidate_info)  # Store candidate info

            contributions = fetch_contributions(api_key, candidate_id, start_date, end_date)
            
            if contributions:
                store_contributions_in_sqlite(db_path, candidate_id, contributions)
            else:
                print(f"No contributions found for {candidate_name}")
        else:
            print(f"Could not find candidate information for {candidate_name}")

if __name__ == "__main__":
    main()
