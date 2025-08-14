1) clean_candidate_names.csv file has the names of the political candidates cleaned (removed designation, whitespace and unsupported characters).
2) SQLtable.py contains code used to create the SQL table 
3) scraping_candidates_sql_indiv is the initial code used to test if scraping for candidate and storing in sqlLite local Database worked
4) fns_scraping_candidates_list has all the functions necessary to fetch the list of candidates from the below code.
5) scraping_candidates_list_parallelization is used to scrape for candidates. I used Parallelazation of the processor to scrape faster, and with fewer API calls. 
The current dataset is restricted to the timeframe of 2022-2024.
