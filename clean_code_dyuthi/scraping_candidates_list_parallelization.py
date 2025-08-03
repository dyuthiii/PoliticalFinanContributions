# -*- coding: utf-8 -*-
"""
Parallelized Code for Candidate Processing
"""

# from pandarallel import pandarallel
# import requests
# import sqlite3
# import os
# from dotenv import load_dotenv
# from datetime import datetime
# import time
# import pandas as pd
# from new_scraping_candidates_list import *

# # Load environment variables
# load_dotenv()

# def process_candidate(candidate_name):
#     """
#     Process a single candidate: search for candidate information, fetch contributions,
#     and store both in the SQLite database.
#     """
#     from new_scraping_candidates_list import search_candidate, fetch_contributions, store_candidate_in_sqlite,store_contributions_in_sqlite
#     import os
#     api_key = os.getenv("FEC_API_KEY")
#     if not api_key:
#         print("Error: FEC API key not found in environment variables.")
#         return
    
#     db_path = 'C:/Users/spark/OneDrive/Desktop/Poli_bot/Poli_bot_DB_final.db'
#     start_date = "01/01/2023"
#     end_date = "11/11/2024"

#     candidate_info = search_candidate(api_key, candidate_name)
#     if candidate_info:
#         candidate_id = candidate_info['candidate_id']
#         store_candidate_in_sqlite(db_path, candidate_info)
        
#         contributions = fetch_contributions(api_key, candidate_id, start_date, end_date)
#         if contributions:
#             store_contributions_in_sqlite(db_path, candidate_id, contributions)
#         else:
#             print(f"No contributions found for {candidate_name}")
#     else:
#         print(f"Could not find candidate information for {candidate_name}")

# def main():
#     """
#     Main function to process candidates in parallel.
#     """
#     try:
#         candidate_df = pd.read_csv("C:/Users/spark/OneDrive/Desktop/Poli_bot/Poli_bot Spyder/background_13Dec.csv")
#     except FileNotFoundError:
#         print("Error: CSV file not found.")
#         return
#     except KeyError:
#         print("Error: 'name' column not found in the CSV file.")
#         return
    
#     # Initialize pandarallel
#     pandarallel.initialize(progress_bar=True)

#     # Parallelize candidate processing
#     start_time = time.time()
#     candidate_df['name'].parallel_apply(process_candidate)
#     end_time = time.time()

#     print(f"Parallel processing completed in {end_time - start_time:.2f} seconds")

# if __name__ == "__main__":
#     main()




# -*- coding: utf-8 -*-
"""
Parallelized Code for Candidate Processing with Database Check
"""

from pandarallel import pandarallel
import requests
import sqlite3
import os
from dotenv import load_dotenv
from datetime import datetime
import time
import pandas as pd
from fns_scraping_candidates_list import *


# Load environment variables
load_dotenv()


def process_candidate(candidate_name):
    """
    Process a single candidate:
    - Check if the candidate exists in the database.
    - If not, fetch their data and store it in the database.
    """
    from fns_scraping_candidates_list import candidate_exists_in_db, search_candidate, fetch_contributions, store_candidate_in_sqlite,store_contributions_in_sqlite
    import os
    api_key = os.getenv("FEC_API_KEY")
    if not api_key:
        print("Error: FEC API key not found in environment variables.")
        return
    
    db_path = 'C:/Users/spark/OneDrive/Desktop/Poli_bot/Poli_bot_DB_final.db'
    start_date = "01/01/2023"
    end_date = "11/11/2024"

    # Check if candidate exists in the database
    if candidate_exists_in_db(db_path, candidate_name):
        print(f"Candidate {candidate_name} already exists in the database. Skipping API call.")
        return
    
    # Fetch and store candidate data if not already in the database
    candidate_info = search_candidate(api_key, candidate_name)
    if candidate_info:
        candidate_id = candidate_info['candidate_id']
        store_candidate_in_sqlite(db_path, candidate_info)
        
        contributions = fetch_contributions(api_key, candidate_id, start_date, end_date)
        if contributions:
            store_contributions_in_sqlite(db_path, candidate_id, contributions)
        else:
            print(f"No contributions found for {candidate_name}")
    else:
        print(f"Could not find candidate information for {candidate_name}")

def main():
    """
    Main function to process candidates in parallel, checking the database first.
    """
    
    # Use the detected encoding to read the CSV
    try:
        candidate_df = pd.read_csv("C:/Users/spark/OneDrive/Desktop/Poli_bot/Poli_bot Spyder/clean_candidate_names.csv", encoding='utf-8',
                                   encoding_errors='replace') 
        #Windows-1248 'ignore', then changed to 'replace'; then utf-8 'ignore' and 'replace' 
    except FileNotFoundError:
        print("Error: CSV file not found.")
        return
    except KeyError:
        print("Error: 'name' column not found in the CSV file.")
        return
    
    # Initialize pandarallel
    pandarallel.initialize(progress_bar=True)

    # Parallelize candidate processing
    start_time = time.time()
    candidate_df['name'].parallel_apply(process_candidate)
    end_time = time.time()

    print(f"Parallel processing completed in {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    main()
#Ran this multiple times to get data into db-- error 'ValueError: too many values to unpack (expected 2)'