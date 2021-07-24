# CampaignFinanceDataPipeline
Data Pipeline for NC Campaign Finance Dashboard

Docker folder contains a simplified environment to run the backend environment and experiments

Python scripts based on Mikhail Yuryevich Bilenko's Ph.D. dissertation: Learnable Similarity Functions and their Application to Record Linkage and Clustering.

The Python scripts are Jupyter Notebooks, but should be easily converted to an inloine python script.

## Create a directory for the Python scrips
## Create a data subdirectory to import the files obtained from NCSBE

1. Data - http://nc-campaign-finance-storage.s3-website-us-east-1.amazonaws.com/
   * active_committee_list
   * committee_doc_list
   * committee_list
   * raw_files

## The scripts are meant to be run in order
  
    * 00 - Download Dataset - downloads the raw files
    * 01 - Preprocess - imports the raw files, sets up the Postgres tables and preps the data for dedupe
    * 02 - Dedupe - this is a actual part that goes over the entire universe of donors and payees and determines if they are the same despite speeling and missing information
    * 03 - Post Dedupe - this creates the views, copies the canonical ids to the transactions and parses out the various sources of committee information to determine party, candidate and active years
    * 04 - Import Election History - Imports the various election return files by candidate/race/precinct and count of vote type according to the data produced by the NCSBE since 2000
