# Google Ngram WSD algorithm test data

Test file, test data cache database and final results are located in test_data folder.
* Sqlite cache database is named cache_combined.sqlite3. This file is can be specified in cachehandler.py file to make it use this database as cache
* Final results are in folder final_results. The folder contains 242 different test runs, each performed with different parameters.
* testfile_for_ngram.csv is test package containing all (over 90) tests in csv format. This file is inputted as parameter to test.py to make it run testing automatically.

Figures calculated from that data are contained in figures folder. Figures are divided to 4 folders, each representing content of test_data/final_results in different way.
