Simple wikify algorithm for natural language processing course

to run you need the wikipedia api package (https://pypi.org/project/wikipedia/), install e.g. 'pip install wikipedia'

to run: python3 wikify.py 'corpus text context etc as string with no new lines' 'disambiguateMeWord'

for testing the wikification run wikify_test.py which will run through the test cases from ../testing/combined/testfile_all_blocks_testfile_all_blocks_combined_and_cleaned.csv
To evaluate the results you can use the wikify_evaluate_results.csv which takes in the correct results which it should've found (validationResults.csv) and a file with the results (in the format that is results_for_validation.csv), this will output the accuracy for the results.