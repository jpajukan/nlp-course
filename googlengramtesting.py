from google_ngram_downloader import readline_google_store

from google_ngram_downloader.__main__ import cooccurrence

#from google_ngram_downloader.__main__ import *

import google_ngram_downloader.__main__



import gzip
import sys
from collections import OrderedDict
from itertools import islice

from opster import Dispatcher
from py.path import local

from google_ngram_downloader.util import iter_google_store, readline_google_store, count_coccurrence

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
    # When records in file=5000000 it is still reasonable calculation time (under 1 min with laptop i7-3630QM)
    # When records in file=50000000 (which is also default value) it is taking like 6 mins
    # Not bothering to try with any more bigger ones

    # With 5-grams
    # Produced files must be exracted before it can be read/analysed with text editor
    # Do we have to copy method and analyse results in inner matrix and not using any output files?

    #cooccurrence(ngram_len=5, verbose=True, records_in_file=50000000)


    # With 2-grams
    # Quite same time than with 5 grams
    cooccurrence(ngram_len=2, verbose=True, records_in_file=5000000)
    #cooccurrence(ngram_len=2, verbose=True, records_in_file=50000000)

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
    fname, url, records = next(readline_google_store(ngram_len=5, indices=["ab"], verbose=True))
    while True:
        print(next(records))


def modded_cooccurence_function():
    #idea is to be similar than original, but limit search to only 1 word

    ngram_len = 2
    output = 'downloads/google_ngrams/{ngram_len}_cooccurrence'
    verbose = True,
    rewrite = False
    records_in_file = 5000000
    lang = 'eng'

    indices = ["te"]


    """Write the cooccurrence frequencies of a word and its contexts."""
    assert ngram_len > 1
    output_dir = local(output.format(ngram_len=ngram_len))
    output_dir.ensure_dir()

    for fname, _, all_records in readline_google_store(ngram_len, lang=lang, verbose=verbose, indices=indices):
        print("hep1")
        postfix = 0
        while (True):
            print("hep2")
            records = islice(all_records, records_in_file)
            print("hep3")
            output_file = output_dir.join(
                '{fname}_{postfix}.gz'.format(
                    fname=fname,
                    postfix=postfix,
                )
            )

            if not rewrite and output_file.check():
                if verbose:
                    print('Skipping {} and the rest...'.format(output_file))
                break
            print("hep4")
            index = OrderedDict()
            print("hep5")
            cooccurrence = count_coccurrence(records, index)
            print("hep6")

            if not cooccurrence:
                break

            id2word = list(index)

            # Do not output if word is not 'test'
            items = (u'{}\t{}\t{}\n'.format(id2word[i], id2word[c], str(v)) for (i, c), v in cooccurrence.items() if id2word[i]=="test" or id2word[c]=="test")

            with gzip.open(str(output_file), 'wb') as f:
                if verbose:
                    print('Writing {}'.format(output_file))
                for item in items:
                    f.write(item.encode('utf8'))

            postfix += 1