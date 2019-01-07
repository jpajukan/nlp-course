Simple wikify algorithm for natural language processing course.

Requires the wikipedia api package (https://pypi.org/project/wikipedia/), install e.g. 'pip install wikipedia'

To run: python3 wikify.py 'corpus text context etc as string with no new lines' 'disambiguateMeWord'

For testing the wikification tool run wikify_test.py which will by default run through the test cases from ../ngram/test_data/testfile_for_ngram.csv. To evaluate the results you can use the wikify_evaluate_results.py which takes in the correct results which it should've found (validationResults.csv) and a file with the results (in the format that is results_for_validation.csv), this will output the accuracy for the results.
