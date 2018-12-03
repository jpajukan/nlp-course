from google_ngram_downloader import readline_google_store

from google_ngram_downloader.__main__ import cooccurrence

import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#from google_ngram_downloader.__main__ import *

import google_ngram_downloader.__main__



import gzip
import sys
from collections import OrderedDict
from itertools import islice


from opster import Dispatcher
from py.path import local

from google_ngram_downloader.util import iter_google_store, readline_google_store, count_coccurrence

from google_ngram_downloader.util import *

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

    #ngram_len = 2
    ngram_len = 5
    output = 'downloads/google_ngrams/{ngram_len}_cooccurrence'
    verbose = True
    rewrite = False
    records_in_file = 50000000
    lang = 'eng'

    indices = ["te"]


    """Write the cooccurrence frequencies of a word and its contexts."""
    assert ngram_len > 1
    output_dir = local(output.format(ngram_len=ngram_len))
    output_dir.ensure_dir()

    #for fname, _, all_records in readline_google_store(ngram_len, lang=lang, verbose=verbose, indices=indices):
    for fname, _, all_records in readline_google_store_modded(ngram_len, lang=lang, verbose=verbose, indices=indices):
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
            #cooccurrence = count_coccurrence(records, index)
            cooccurrence = count_coccurrence_modded(records, index)
            print("hep6")

            if not cooccurrence:
                break

            id2word = list(index)

            # Do not output if word is not 'test'
            #items = (u'{}\t{}\t{}\n'.format(id2word[i], id2word[c], str(v)) for (i, c), v in cooccurrence.items() if id2word[i]=="test" or id2word[c]=="test")
            items = (u'{}\t{}\t{}\n'.format(id2word[i], id2word[c], str(v)) for (i, c), v in cooccurrence.items())

            with gzip.open(str(output_file), 'wb') as f:
                if verbose:
                    print('Writing {}'.format(output_file))
                for item in items:
                    f.write(item.encode('utf8'))

            postfix += 1

def count_coccurrence_modded(records, index):
    print("hep7")
    #filtering everything that is not test started
    #filtered_records = filter(lambda r: r.ngram.startswith("test "), records)

    #grouped_records = groupby(filtered_records, key=lambda r: r.ngram)
    grouped_records = groupby(records, key=lambda r: r.ngram)

    print("hep8")


    ngram_counts = ((ngram, sum(r.match_count for r in records)) for ngram, records in grouped_records)
    #ngram_counts = ((ngram, sum(r.match_count for r in records)) for ngram, records in grouped_records if ngram.startswith("test"))
    #ngram_counts = ((ngram, sum(r.match_count for r in records)) for ngram, records in grouped_records)
    print("hep9")
    cooc = (ngram_to_cooc(ngram, count, index) for ngram, count in ngram_counts)
    print("hep10")
    counter = collections.Counter()
    for item, count in chain.from_iterable(cooc):
        #print(item)
        counter[item] += count
    print("hep11")
    return counter

#def readline_google_store_modded(ngram_len, lang='eng', indices=None, chunk_size=1024 ** 2, verbose=False):
def readline_google_store_modded(ngram_len, lang='eng', indices=None, chunk_size=2048 ** 2, verbose=False):
    """Iterate over the data in the Google ngram collectioin.
        :param int ngram_len: the length of ngrams to be streamed.
        :param str lang: the langueage of the ngrams.
        :param iter indices: the file indices to be downloaded.
        :param int chunk_size: the size the chunks of raw compressed data.
        :param bool verbose: if `True`, then the debug information is shown to `sys.stderr`.
        :returns: a iterator over triples `(fname, url, records)`
    """

    for fname, url, request in iter_google_store(ngram_len, verbose=verbose, lang=lang, indices=indices):
        dec = zlib.decompressobj(32 + zlib.MAX_WBITS)

        def lines():
            last = b''
            compressed_chunks = request.iter_content(chunk_size=chunk_size)

            for i, compressed_chunk in enumerate(compressed_chunks):
                chunk = dec.decompress(compressed_chunk)

                lines = (last + chunk).split(b'\n')
                lines, last = lines[:-1], lines[-1]

                for line in lines:
                    line = line.decode('utf-8')
                    data = line.split('\t')
                    assert len(data) == 4
                    ngram = data[0]
                    #print(ngram)
                    #remove everything that is not test
                    if not ngram.startswith("test "):
                        continue

                    other = map(int, data[1:])
                    yield Record(ngram, *other)

            if last:
                raise StreamInterruptionError(
                    url,
                    "Data stream ended on a non-empty line. This might be due "
                    "to temporary networking problems.")

        yield fname, url, lines()


def build_contextual_wording(word):
    """

    :param word: input synset of where contextual wording must be built
    :return: array of contextual words as strings
    """
    lemma = word.lemma_names()

    # Adding also hyponyms hypernyms meronyms and holonyms?

    hypernyms = word.hypernyms()

    hypernyms_lemmas = []

    for hp in hypernyms:
        hypernyms_lemmas.extend(hp.lemma_names())

    hyponyms = word.hyponyms()

    hyponyms_lemmas = []

    for hyms in hyponyms:
        hyponyms_lemmas.extend(hyms.lemma_names())

    holonyms = word.member_holonyms()

    holonyms_lemmas = []

    for homs in holonyms:
        holonyms_lemmas.extend(homs.lemma_names())

    meronyms = word.part_meronyms()

    meronyms_lemmas = []

    for mems in meronyms:
        meronyms_lemmas.extend(mems.lemma_names())

    contextual_wording = []

    contextual_wording.extend(lemma)
    contextual_wording.extend(hypernyms_lemmas)
    contextual_wording.extend(hyponyms_lemmas)
    contextual_wording.extend(holonyms_lemmas)
    contextual_wording.extend(meronyms_lemmas)

    end_result = []

    for word in contextual_wording:
        result = word.split("_")
        end_result.extend(result)

    end_result = set(end_result)
    return end_result


def cooccurence_bank(contextual_words):
    # get 5 gram co-occurence matrix of bank and then do some calculations to sentences

    # ngram_len = 2
    ngram_len = 5
    output = 'downloads/google_ngrams/{ngram_len}_cooccurrence'
    verbose = True
    rewrite = False
    #records_in_file = 50000000
    records_in_file = 5000000
    lang = 'eng'

    indices = ["ba"]

    word = "bank"

    """Write the cooccurrence frequencies of a word and its contexts."""
    assert ngram_len > 1
    output_dir = local(output.format(ngram_len=ngram_len))
    output_dir.ensure_dir()

    for fname, _, all_records in readline_google_store(ngram_len, lang=lang, verbose=verbose, indices=indices):
    #for fname, _, all_records in readline_google_store_modded(ngram_len, lang=lang, verbose=verbose, indices=indices):
        postfix = 0
        while (True):
            records = islice(all_records, records_in_file)
            #output_file = output_dir.join(
            #    '{fname}_{postfix}.gz'.format(
            #        fname=fname,
           #         postfix=postfix,
            #    )
            #)

            #if not rewrite and output_file.check():
            #    if verbose:
            #        print('Skipping {} and the rest...'.format(output_file))
            #    break
            index = OrderedDict()
            cooccurrence = count_coccurrence(records, index)
            #cooccurrence = count_coccurrence_modded(records, index)

            if not cooccurrence:
                break

            id2word = list(index)

            # Do not output if word is not 'test'
            # items = (u'{}\t{}\t{}\n'.format(id2word[i], id2word[c], str(v)) for (i, c), v in cooccurrence.items() if id2word[i]=="test" or id2word[c]=="test")
            #items = (u'{}\t{}\t{}\n'.format(id2word[i], id2word[c], str(v)) for (i, c), v in cooccurrence.items())

            #with gzip.open(str(output_file), 'wb') as f:
            #    if verbose:
            #        print('Writing {}'.format(output_file))
            #    for item in items:
            #        f.write(item.encode('utf8'))

            #postfix += 1

            # Print this rounds results
            for (i, c), v in cooccurrence.items():
                if id2word[i] == word:
                    if id2word[c] in contextual_words:
                        print("words " + id2word[i] + " " + id2word[c] + " " + "cooccurence amount: " +str(v))
                elif id2word[c] == word:
                    if id2word[i] in contextual_words:
                        print("words " + id2word[i] + " " + id2word[c] + " " + "cooccurence amount: " +str(v))

def prepare_context_sentence(sentence, word):

    # removes stopwords and target word
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(sentence)

    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words and not (w == word):
            filtered_sentence.append(w)

    #print(filtered_sentence)
    return filtered_sentence

