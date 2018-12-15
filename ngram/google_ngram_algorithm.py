from itertools import islice, product

from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from ast import literal_eval
from pandas import DataFrame  # http://github.com/pydata/pandas
import pandas as pd
import re
import requests               # http://github.com/kennethreitz/requests

from time import sleep

# Muistettava mainita mistä otettu lainakoodit

corpora = dict(eng_us_2012=17, eng_us_2009=5, eng_gb_2012=18, eng_gb_2009=6,
               chi_sim_2012=23, chi_sim_2009=11, eng_2012=15, eng_2009=0,
               eng_fiction_2012=16, eng_fiction_2009=4, eng_1m_2009=1,
               fre_2012=19, fre_2009=7, ger_2012=20, ger_2009=8, heb_2012=24,
               heb_2009=9, spa_2012=21, spa_2009=10, rus_2012=25, rus_2009=12,
               ita_2012=22)


# https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


class GoogleNgramAlgorithm:
    def __init__(self, target_word, target_context, sense_wording_size=12, target_context_size=6):
        """
        :param target_word: word to be disambiguated, for now we suggest that there is no duplicate target words
        :param targe_tcontext: context of target word as string
        :param sense_wording_size: number of words in sense which will be created for every synset
        :param target_context_size: number of words which will be taken from context wording
        """

        self.target_word = target_word
        self.target_context = target_context
        self.target_context_processed = []
        self.sense_wording_size = sense_wording_size
        self.target_context_size = target_context_size

    def create_sense_wording(self, synset):
        """
        :param synset: synset to which different sense words are created
        :return:
        """

        # Add hypernyms, hyponyms, holonyms and meronyms to single list
        lemma = synset.lemma_names()

        hypernyms = synset.hypernyms()
        hypernyms_lemmas = []

        for hp in hypernyms:
            hypernyms_lemmas.extend(hp.lemma_names())

        hyponyms = synset.hyponyms()
        hyponyms_lemmas = []
        for hyms in hyponyms:
            hyponyms_lemmas.extend(hyms.lemma_names())

        holonyms = synset.member_holonyms()
        holonyms_lemmas = []
        for homs in holonyms:
            holonyms_lemmas.extend(homs.lemma_names())

        meronyms = synset.part_meronyms()
        meronyms_lemmas = []
        for mems in meronyms:
            meronyms_lemmas.extend(mems.lemma_names())

        contextual_wording = []

        contextual_wording.extend(lemma)
        contextual_wording.extend(hypernyms_lemmas)
        contextual_wording.extend(hyponyms_lemmas)
        contextual_wording.extend(holonyms_lemmas)
        contextual_wording.extend(meronyms_lemmas)

        print(contextual_wording)
        end_result = []

        for word in contextual_wording:
            if "_" in word:
                result = word.split("_")
                for w in result:
                    if w not in end_result:
                        end_result.append(w)
            else:
                if word not in end_result:
                    end_result.append(word)


        end_result_filtered = []

        # Remove if target word and stopwords from list
        stop_words = set(stopwords.words('english'))

        for word in end_result:
            if word not in stop_words and word != self.target_word:
                end_result_filtered.append(word)

        #print(end_result_filtered)
        # Crudely just take fist of the list as context words
        if len(end_result_filtered) > self.sense_wording_size:
            return end_result_filtered[:self.sense_wording_size]

        return end_result_filtered


    def create_target_context_wording(self):
        """
        Just removes stopwords and takes amount of sensible context words according to target_context_size parameter
        :return:
        """
        # removes stopwords and target word
        stop_words = set(stopwords.words('english'))

        word_tokens = word_tokenize(self.target_context)

        stopword_filtered_sentence = []
        for w in word_tokens:
            if w not in stop_words:
                stopword_filtered_sentence.append(w)

        context_wording = []

        # Take contex wording as close as possible from target word in context by getting contex wording around target word

        distance = 1
        target_word_index = stopword_filtered_sentence.index(self.target_word)

        new_words_found = True

        while new_words_found:
            new_words_found = False
            if len(context_wording) < self.target_context_size:
                contexword_index1 = target_word_index + distance
                contexword_index2 = target_word_index - distance

                if contexword_index1 > 0 and contexword_index1 < len(stopword_filtered_sentence):
                    context_wording.append(stopword_filtered_sentence[contexword_index1])
                    new_words_found = True

                if len(context_wording) < self.target_context_size:
                    if contexword_index2 > 0 and contexword_index2 < len(stopword_filtered_sentence):
                        context_wording.append(stopword_filtered_sentence[contexword_index2])
                        new_words_found = True

                distance += 1
            else:
                break

        self.target_context_processed = context_wording

    def prepare(self):
        """
        Prepares target context and possible senses and synset wordings for them
        :return:
        """

        # Process target context wording
        self.create_target_context_wording()

        self.data = []
        synsets = wn.synsets(self.target_word)

        for synset in synsets:
            # Create sense wording for this synset
            sense_wording = self.create_sense_wording(synset)

            # Create all bigrams

            #print(synset)
            #print(sense_wording)
            #print(self.target_context_processed)

            bigrams = list(product(sense_wording, self.target_context_processed))
            bigrams.extend(list(product(self.target_context_processed, sense_wording)))

            #print(bigrams)
            #exit()

            # Remove duplicates
            bigrams = list(set(bigrams))

            # Create data dict and save for other usage
            sense_data = {}
            sense_data['synset'] = synset
            sense_data['sense_wording'] = self.create_sense_wording(synset)
            sense_data['query_bigrams'] = bigrams
            sense_data['query_results'] = pd.DataFrame()
            sense_data['score'] = 0

            self.data.append(sense_data)


    def query_google_ngram(self):
        """
        Query everything and save results to
        :return:
        """

        corpus, startYear, endYear, smoothing = 'eng_2012', 1800, 2000, 1
        printHelp, caseInsensitive, allData = False, False, False
        toSave, toPrint, toPlot = True, True, False

        for sense in self.data:

            # Make query always with 12 bigrams because it seems like max amount

            bigrams_chunked = chunks(sense['query_bigrams'], 12)

            for bigram_chunk in bigrams_chunked:
                query = self.create_query_string(bigram_chunk)
                print("Querying with ngrams %s" % (query))
                url, urlquery, df = self.getNgrams(query, corpus, startYear, endYear, smoothing, caseInsensitive)
                sense['query_results'] = pd.concat([sense['query_results'], df])

    def create_query_string(self, bigrams):
        query = bigrams[0][0] + " " + bigrams[0][1]

        for bigram in bigrams[1:]:
            query = query + "," + bigram[0] + " " + bigram[1]

        return query

    def analyze(self):
        """
        Score every synset and return information
        :return:
        """

        # Now only with simple scoring analysis, should be better later

        #print(self.data[0]['query_results'])

        for sense in self.data:
            score = 0
            for bigram in sense['query_bigrams']:
                key = bigram[0] + " " + bigram[1]

                if key in sense['query_results']:
                    score += sense['query_results'][key].sum()


            # Lets divide score by all bigram count

            if len(sense['query_bigrams']) == 0:
                sense['score'] = 0
            else:
                sense['score'] = score / len(sense['query_bigrams'])

    def print_results(self):
        """
        Function to simply just print results. Might be futile
        :return:
        """

        for sense in self.data:
            print(sense['synset'])
            print(sense['synset'].lemma_names())
            print(str(sense['score']))
            print("\n")

    def get_all_data(self):
        """
        :return: Returns all data as huge chunk
        """
        return self.data

    def get_all_results(self):
        """
        :return: Returns all interesting results (synset, synset lemma names and score) ordered by score
        """
        sorted_results = sorted(self.data, key=lambda x: x['score'], reverse=True)

        result_tuples = []

        for result in sorted_results:
            result_tuples.append((result['synset'], result['synset'].lemma_names(), result['synset'].definition(), result['score']))

        return result_tuples

    def getNgrams(self, query, corpus, startYear, endYear, smoothing, caseInsensitive):
        params = dict(content=query, year_start=startYear, year_end=endYear,
                      corpus=corpora[corpus], smoothing=smoothing,
                      case_insensitive=caseInsensitive)
        if params['case_insensitive'] is False:
            params.pop('case_insensitive')
        if '?' in params['content']:
            params['content'] = params['content'].replace('?', '*')
        if '@' in params['content']:
            params['content'] = params['content'].replace('@', '=>')

        retry_wait_time = 0

        # TODO: Program jams if there is no internet connection and 200 response is never received
        while True:
            req = requests.get('http://books.google.com/ngrams/graph', params=params)

            if req.status_code == 200:
                res = re.findall('var data = (.*?);\\n', req.text)
                if res:
                    data = {qry['ngram']: qry['timeseries']
                            for qry in literal_eval(res[0])}
                    df = DataFrame(data)
                    df.insert(0, 'year', list(range(startYear, endYear + 1)))
                else:
                    df = DataFrame()

                break

            if req.status_code == 429:
                # TODO: Rude way now, could this be improved by lookin for response retry-after header?
                retry_wait_time += 10
                print("Response 429 received, waiting %s seconds" % (retry_wait_time))
                sleep(retry_wait_time)

        return req.url, params['content'], df
