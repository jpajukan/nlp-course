from google_ngram_downloader import readline_google_store

from google_ngram_downloader.__main__ import cooccurrence
"""

This file contains only testing and playing around.

Purpose is only to familiarize ourselves to this ngram stuff and know what can be done with it

This file is removed when no longer needed

"""

def ngram_wiki_example():
    fname, url, records = next(readline_google_store(ngram_len=5))
    print(fname)
    print(url)
    print(next(records))

def ngram_cooccurence_example():
    # Seems quite heavy... I dont even know if this does any shit

    # Think this tries to download all 5-grams. Which are together like over 200 GB...
    cooccurrence(ngram_len=5, verbose=True)

def ngram_example2(word):
    # https://www.quora.com/Is-there-any-Google-Ngram-API-for-Python

    count = 0
    fname, url, records = next(readline_google_store(ngram_len=1, indices=word[0]))

    try:
        record = next(records)
        print(record)
        while record.ngram != word:
            record = next(records)
            print(record)

        while record.ngram == word:
            count = count + record.match_count
            record = next(records)
            print(record)

        print(count)
    except StopIteration:
        pass

def ngram_example_5_gram():

    # Starts looking 5-grams from file aa
    fname, url, records = next(readline_google_store(ngram_len=5, indices=["aa"], verbose=True))
    while True:
        print(next(records))
