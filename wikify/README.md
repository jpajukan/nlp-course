Simple wikify algorithm for natural language processing course

wikify.py   -   a really simple implementation that just loops through the given corpus and wikifies every word. Takes the first given result from Wikipedia API, no logic behind the link chosen other than that.

wikify2_0.py    -   same result as wikify.py but a bit differently done

wikify3.py  -   The real deal! *Slaps on the roof* This bad boy can wikify (disambiguate) any word against a given corpus by calculating a similarity score (from 0 to 1) between the corpus and the resulting Wikipedia pages based on the word search.

to run: python3 wikify3.py 'corpus text context etc as string with no new lines' 'disambiguateMe'
