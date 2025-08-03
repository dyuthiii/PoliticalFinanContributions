# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 18:44:34 2024

@author: spark
"""
import sqlite3
db_path = "C:/Users/spark/OneDrive/Desktop/Poli_bot/Poli_bot_DB_final.db"
def create_contributions_table(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
   CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    candidate_name TEXT,
    candidate_id TEXT UNIQUE,
    name TEXT,
    party TEXT,
    party_full TEXT,
    state TEXT,
    district TEXT,
    district_number INTEGER,
    office TEXT,
    office_full TEXT,
    incumbent_challenge TEXT,
    incumbent_challenge_full TEXT,
    candidate_status TEXT,
    active_through INTEGER,
    candidate_inactive BOOLEAN,
    has_raised_funds BOOLEAN,
    federal_funds_flag BOOLEAN,
    first_file_date TEXT,
    last_file_date TEXT,
    last_f2_date TEXT,
    load_date TEXT,
    cycles TEXT,
    election_years TEXT,
    election_districts TEXT,
    inactive_election_years TEXT,
    principal_committees TEXT
)
    ''')
    
    conn.commit()
    conn.close()

# Usage
create_contributions_table(db_path)