from itertools import islice, product

from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from ast import literal_eval
from pandas import DataFrame
import pandas as pd
import re
import requests
import csv

from time import sleep

import math

from cachehandler import *

corpora = dict(eng_us_2012=17, eng_us_2009=5, eng_gb_2012=18, eng_gb_2009=6,
               chi_sim_2012=23, chi_sim_2009=11, eng_2012=15, eng_2009=0,
               eng_fiction_2012=16, eng_fiction_2009=4, eng_1m_2009=1,
               fre_2012=19, fre_2009=7, ger_2012=20, ger_2009=8, heb_2012=24,
               heb_2009=9, spa_2012=21, spa_2009=10, rus_2012=25, rus_2009=12,
               ita_2012=22)


# From https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


class GoogleNgramAlgorithm:
    def __init__(self, target_word, target_context, sense_wording_size=12, target_context_size=6, use_wildcards=False):
        """
        :param target_word: word to be disambiguated, for now we suggest that there is no duplicate target words
        :param targe_tcontext: context of target word as string
        :param sense_wording_size: number of words in sense which will be created for every synset
        :param target_context_size: number of words which will be taken from context wording
        :param use_wildcards: if algorithm builds also wildcard trigrams during
        """

        self.target_word = target_word
        self.target_context = target_context
        self.target_context_processed = []
        self.sense_wording_size = sense_wording_size
        self.target_context_size = target_context_size
        self.use_wildcards = use_wildcards

        # Counting absolute amount of words from http: // stanford.edu / ~risi / tutorials / absolute_ngram_counts.html

        total_words_data = " 	1505,32059,231,1	1507,49586,477,1	1515,289011,2197,1	1520,51783,223,1	1524,287177,1275,1	1525,3559,69,1	1527,4375,39,1	1541,5272,59,1	1563,213843,931,1	1564,70755,387,1	1568,153095,1124,2	1572,177484,797,1	1574,62235,689,1	1575,186706,1067,1	1579,203074,1143,3	1581,708458,2824,6	1582,151000,537,1	1584,151925,393,1	1587,248361,762,2	1588,41548,634,2	1589,36290,238,2	1590,564921,2260,2	1592,96955,814,4	1593,39997,328,2	1594,11106,67,1	1595,33664,347,3	1597,10923,101,1	1598,85051,768,2	1600,405205,985,1	1602,3292,47,1	1603,69050,561,1	1605,14493,131,1	1606,62921,601,3	1607,381763,1600,2	1610,6258,75,1	1611,49641,457,1	1612,52898,593,1	1614,8777,57,1	1618,20166,147,1	1619,55192,467,1	1620,229054,2371,3	1621,64197,679,3	1623,120443,896,2	1624,145470,899,3	1625,69296,551,1	1626,41890,259,1	1628,6425,43,1	1629,288773,1250,2	1630,152568,1463,3	1631,474458,1899,1	1632,43064,299,1	1634,141378,777,3	1635,244673,1385,3	1636,31714,252,2	1637,681719,2315,3	1638,243942,876,2	1640,60550,425,3	1641,45397,536,2	1642,137346,769,3	1643,177489,1238,6	1644,1018174,4031,5	1645,252714,1263,3	1646,55522,253,1	1647,312270,2015,5	1648,458975,2306,4	1649,260987,1796,4	1650,192820,1161,7	1651,540758,2221,3	1652,168692,1023,3	1653,379618,2677,7	1654,36496,256,2	1655,280899,1789,5	1656,688699,3142,4	1657,310453,2551,5	1658,834659,4509,9	1659,543657,2331,3	1660,130457,1085,5	1661,128825,931,3	1662,239762,1471,3	1663,208750,2021,5	1664,290743,2670,6	1665,269608,2689,11	1666,81564,843,3	1667,751217,3449,9	1668,1065563,3920,6	1669,342820,2276,4	1670,734354,3127,5	1671,149851,1276,4	1672,425998,2665,5	1673,935178,5517,11	1674,126602,643,3	1675,1644156,8918,14	1676,1801615,8433,15	1677,799238,5380,12	1678,1966870,8516,18	1679,1112022,6347,13	1680,1099854,6122,22	1681,2614565,11444,28	1682,3667945,15570,30	1683,4175428,15946,30	1684,1707625,8701,19	1685,2350253,14504,28	1686,1263478,8862,22	1687,1185730,4521,13	1688,2548272,10593,21	1689,982547,6474,20	1690,909320,5392,14	1691,321865,2262,8	1692,1674892,8524,14	1693,1038415,7426,16	1694,2020553,13199,25	1695,1223730,8829,13	1696,829773,7095,21	1697,947914,4401,9	1698,3115797,19918,38	1699,2830668,17088,36	1700,3724080,23837,37	1701,3969408,26769,49	1702,4981091,27197,65	1703,4160884,26829,47	1704,4896743,30972,68	1705,4908749,28840,60	1706,6717731,36302,70	1707,5350926,26228,52	1708,6481151,37416,70	1709,3354295,24260,56	1710,6947443,35889,99	1711,6737146,40069,85	1712,3822481,22378,58	1713,4720647,25961,77	1714,7764527,42791,95	1715,6381321,40575,91	1716,5059979,23970,70	1717,6932237,37712,90	1718,5184576,36292,92	1719,4957704,30204,98	1720,9307091,51148,102	1721,6991857,37936,84	1722,10462138,45518,96	1723,7650075,43642,106	1724,8504688,53163,91	1725,10634464,54579,99	1726,10049695,66514,106	1727,12961617,73073,133	1728,11203433,72304,142	1729,12290699,65192,122	1730,12141708,69124,140	1731,12939697,67794,128	1732,10191917,66456,144	1733,5729194,33674,98	1734,10069531,62738,120	1735,9078498,59822,130	1736,8049773,47332,112	1737,13254037,74519,133	1738,13711768,67208,132	1739,11506472,73091,169	1740,11351999,63577,123	1741,8036677,50136,122	1742,11481001,68262,142	1743,9480804,68475,165	1744,13999448,86587,171	1745,8964077,62566,184	1746,7178475,42780,142	1747,15862088,87459,177	1748,15326914,83841,153	1749,12651711,88764,196	1750,19252447,105214,218	1751,20150324,112498,218	1752,14340951,87244,182	1753,19100911,113065,229	1754,20408128,131704,220	1755,20284102,135065,257	1756,8734579,59545,165	1757,13717180,93794,194	1758,16974336,104794,196	1759,21275484,125399,205	1760,14620367,104986,216	1761,17721029,107990,212	1762,11334996,73704,158	1763,20103289,111617,195	1764,18680471,112259,201	1765,15656943,101540,196	1766,26832144,166327,279	1767,19968484,137147,239	1768,27116433,186755,307	1769,18548978,128275,237	1770,21906473,156785,287	1771,20026146,148156,242	1772,20087322,151573,259	1773,18809127,131107,233	1774,19376100,140530,286	1775,25217307,163753,297	1776,26766563,182397,333	1777,22531379,164511,291	1778,20822070,130713,211	1779,18344680,132503,247	1780,19284173,137264,262	1781,21534708,165102,272	1782,21505581,148858,256	1783,21001833,154110,278	1784,26735435,196374,310	1785,26424206,195551,333	1786,27701969,201168,328	1787,41147754,274736,406	1788,43010567,317558,476	1789,37991018,274486,408	1790,40363128,290254,448	1791,44446487,303140,450	1792,47305037,334531,525	1793,41628412,306038,536	1794,48633342,334985,503	1795,46129522,306795,481	1796,56007600,402660,600	1797,47048067,327575,527	1798,46311447,317118,520	1799,50259992,358621,543	1800,70784405,481221,669	1801,107290136,720762,976	1802,95731997,593319,843	1803,104173226,703119,941	1804,114051906,773467,1079	1805,115330195,768720,1054	1806,118229517,820253,1139	1807,128904931,843799,1139	1808,129988114,825924,1172	1809,137911980,849578,1188	1810,150961261,942002,1280	1811,177318465,1089707,1425	1812,172538907,966207,1285	1813,144660671,848854,1148	1814,168441689,1005881,1325	1815,156318674,940919,1281	1816,161561836,993399,1375	1817,182422107,1112404,1608	1818,204446854,1249575,1711	1819,174156635,1074883,1603	1820,231277724,1428596,1876	1821,181677006,1090084,1530	1822,271213007,1582135,2049	1823,254327070,1531352,2096	1824,309237910,1818566,2402	1825,318701311,1931153,2571	1826,243758959,1459702,2006	1827,253677933,1540742,2124	1828,273678947,1616864,2320	1829,293815859,1682580,2338	1830,342378710,1893561,2615	1831,313388047,1693686,2458	1832,314184783,1697641,2501	1833,310441320,1768777,2655	1834,301383644,1685631,2585	1835,355491202,2000520,2946	1836,365982104,2016239,2951	1837,337485292,1897476,2642	1838,358600155,1973223,2813	1839,413876708,2268357,3195	1840,423904296,2214894,3196	1841,387286321,2083152,3048	1842,348396317,1825805,2711	1843,404133447,2000337,2899	1844,419311001,2164514,3086	1845,456885448,2327894,3294	1846,459546575,2351443,3305	1847,443868440,2210955,3291	1848,466134080,2417716,3648	1849,472315353,2428935,3539	1850,504143257,2601734,3910	1851,537705793,2787491,4021	1852,558718364,2900999,4461	1853,625159477,3248278,4706	1854,683559348,3445720,4810	1855,605758582,3126226,4404	1856,652385453,3360386,4728	1857,568489706,2971641,4319	1858,541848821,2794762,4108	1859,588343315,3047548,4572	1860,607952196,3291751,4921	1861,463190641,2457516,3664	1862,396839451,2162284,3364	1863,418297294,2280211,3527	1864,493159851,2742669,4089	1865,503022451,2754685,4265	1866,548257863,2970231,4373	1867,518622969,2798144,4168	1868,547590187,3004671,4509	1869,558291347,3052571,4589	1870,548870828,3010658,4588	1871,560339562,3109850,4674	1872,566620105,3133978,4768	1873,583981485,3210707,4799	1874,636667506,3496138,5190	1875,643873731,3513955,5335	1876,676820039,3717671,5691	1877,667722549,3635691,5657	1878,629401874,3475917,5521	1879,654448581,3648960,5912	1880,784223075,4339293,6659	1881,789254798,4377740,6836	1882,828502461,4594461,7295	1883,930196929,5188267,8091	1884,881638914,4821278,7906	1885,857166435,4796652,7804	1886,727723136,3978980,6198	1887,801865869,4578817,7215	1888,795886071,4489400,7054	1889,763170247,4217872,6480	1890,787152479,4446336,7006	1891,849750639,4772590,7600	1892,936056142,5340906,8320	1893,915629979,5204954,8214	1894,899615494,5190068,8132	1895,984856075,5699486,9184	1896,1050921103,6149427,9663	1897,1031909734,6036650,9632	1898,1109257706,6474893,10193	1899,1232717908,7319283,11421	1900,1341057959,7880706,12204	1901,1285712637,7611053,11923	1902,1311315033,7850395,12325	1903,1266236889,7672684,12386	1904,1405505328,8505994,13406	1905,1351302005,7982387,12833	1906,1397090480,8324581,13309	1907,1409945274,8352873,13533	1908,1417130893,8455420,13826	1909,1283265090,7678880,12638	1910,1354824248,8082350,13278	1911,1350964981,8146435,13659	1912,1431385638,8498210,14314	1913,1356693322,8272376,14064	1914,1324894757,8031654,13964	1915,1211361619,7359683,13357	1916,1175413415,7285233,13449	1917,1183132092,7301665,13535	1918,1039343103,6427497,12225	1919,1136614538,6939246,12588	1920,1388696469,8320305,14671	1921,1216676110,7129055,12681	1922,1413237707,8295471,14781	1923,1151386048,6679296,11962	1924,1069007206,6285325,11221	1925,1113107246,6436655,11609	1926,1053565430,6180969,11513	1927,1216023821,6992594,12560	1928,1212716430,6940650,12610	1929,1153722574,6757530,12430	1930,1244889331,7172751,13131	1931,1183806248,6746535,12339	1932,1057602772,5908248,10940	1933,915956659,5193167,10129	1934,1053600093,5813581,10781	1935,1157109310,6383929,11543	1936,1199843463,6704700,12168	1937,1232280287,6867867,12393	1938,1261812592,7006038,12494	1939,1249209591,6860069,12255	1940,1179404138,6458613,11539	1941,1084154164,5943516,10956	1942,1045379066,5652409,10561	1943,890214397,4754157,9221	1944,812192380,4254836,8696	1945,926378706,4754610,9542	1946,1203221497,6293844,12452	1947,1385834769,7297313,14115	1948,1486005621,7719563,14721	1949,1641024100,8474538,15754	1950,1644401950,8581523,15761	1951,1603394676,8369856,15418	1952,1621780754,8271139,15307	1953,1590464886,8243557,15325	1954,1662160145,8642537,16201	1955,1751719755,9009566,16994	1956,1817491821,9289947,17453	1957,1952474329,10050283,18977	1958,1976098333,10184584,19292	1959,2064236476,10667039,20781	1960,2341981521,12110214,24048	1961,2567977722,13168876,25762	1962,2818694749,14534596,27762	1963,2955051696,15289261,29569	1964,2931038992,15327267,30661	1965,3300623502,16925833,32999	1966,3466842517,17885635,35243	1967,3658119990,18856794,37636	1968,3968752101,20713781,40613	1969,3942222509,20605052,40154	1970,4086393350,21493334,42050	1971,4058576649,21022316,41676	1972,4174172415,21723303,43701	1973,4058707895,20934291,42413	1974,4045487401,20870625,42423	1975,4104379941,21163884,43866	1976,4242326406,21741811,44785	1977,4314577619,22131803,45231	1978,4365839878,22337808,45652	1979,4528331460,23121674,47094	1980,4611609946,23399729,47197	1981,4627406112,23181513,46107	1982,4839530894,24286876,48446	1983,4982167985,24855807,49481	1984,5309222580,26493896,52068	1985,5475269397,27311038,53730	1986,5793946882,28860058,56268	1987,5936558026,29600208,57856	1988,6191886939,30977704,60672	1989,6549339038,32665219,64029	1990,7075013106,35252588,69220	1991,6895715366,34521903,68159	1992,7596808027,37580665,72393	1993,7492130348,37154768,71658	1994,8027353540,39575664,76662	1995,8276258599,40863936,77890	1996,8745049453,42919779,82091	1997,8979708108,43952838,84104	1998,9406708249,45989297,87421	1999,9997156197,48914071,91983	2000,11190986329,54799233,103405	2001,11349375656,55886251,104147	2002,12519922882,62335467,117207	2003,13632028136,68561620,127066	2004,14705541576,73346714,139616	2005,14425183957,72756812,138132	2006,15310495914,77883896,148342	2007,16206118071,82969746,155472	2008,19482936409,108811006,206272	"
        total_counts = dict()
        data = csv.reader(total_words_data.split("\t"))

        for row in data:
            # First and last row are empty so exception is needed
            try:
                year = row[0]
                word_count = row [1]
                if int(year) >= 1800 and int(year) <= 2008:
                    total_counts[year] = int(word_count)

            except ValueError:
                pass
            except IndexError:
                pass
        self.total_word_counts = total_counts

        print(self.total_word_counts)

    def create_sense_wording(self, synset):
        """
        :param synset: synset to which different sense words are created
        :return list: specified length list filled with sense wording of synset
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

        # Leaving target word in words
        for word in end_result:
            if word not in stop_words:
                end_result_filtered.append(word)

        # Crudely just take fist of the list as context words
        if len(end_result_filtered) > self.sense_wording_size:
            return end_result_filtered[:self.sense_wording_size]

        print("Sense wording")
        print(end_result_filtered)

        return end_result_filtered


    def create_target_context_wording(self):
        """
        Removes stopwords and takes amount of sensible context words according to target_context_size parameter
        """

        # Remove stopwords and target word
        stop_words = set(stopwords.words('english'))

        word_tokens = word_tokenize(self.target_context)

        # Removing also other unwanted characters
        stopword_filtered_sentence = []
        other_unwanted = ["'s", "' s", "'"]

        for w in word_tokens:
            if w not in stop_words and (w not in other_unwanted):
                stopword_filtered_sentence.append(w)

        stopword_filtered_sentence_lowercase = [item.lower() for item in stopword_filtered_sentence]

        context_wording = []

        # Take context wording as close as possible of target word
        distance = 1
        target_word_index = stopword_filtered_sentence_lowercase.index(self.target_word.lower())

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
            bigrams = list(product(sense_wording, self.target_context_processed))
            bigrams.extend(list(product(self.target_context_processed, sense_wording)))

            # Remove possible duplicates
            bigrams = list(set(bigrams))

            # Create data dict and save for later usage
            sense_data = {}
            sense_data['synset'] = synset
            sense_data['sense_wording'] = self.create_sense_wording(synset)
            sense_data['query_bigrams'] = bigrams
            sense_data['query_results'] = pd.DataFrame()
            sense_data['score'] = 0
            sense_data['absolute_score'] = 0

            self.data.append(sense_data)

    def get_query_bigrams_not_in_cache(self, bigrams, wildcard=False):
        """
        Return list of bigrams which ara not in cache
        :param bigrams: List of bigram tuples to be checked
        :param wildcard: Wheter or not wildcard is used
        :return: List of bigrams not in cache
        """
        not_in_cache = []

        for bg in bigrams:
            result = None

            if wildcard == False:
                ngram = bg[0] + " " + bg[1]
                result = get_cache(ngram)
            else:
                ngram = bg[0] + " * " + bg[1]
                result = get_cache(ngram)

            if result == None:
                not_in_cache.append(bg)

            if result != None:
                pass

        return not_in_cache

    def get_bigram_data_existing_in_cache(self, bigrams, wildcard=False):
        """
        Return dictionary of bigrams scores which are in cache
        :param bigrams: List of bigram tuples to be checked
        :param wildcard: Wheter or not wildcard is used
        :return: Dictionary of bigrams scores in cache
        """
        data = {}

        for bg in bigrams:
            ngram = bg[0] + " " + bg[1]
            result = get_cache(ngram)
            if result != None:
                data[ngram] = result


            if wildcard == True:
                ngram = bg[0] + " * " + bg[1]
                result = get_cache(ngram)
                if result != None:
                    data[ngram] = result
        return data


    def query_google_ngram(self):
        """
        Query every sense queries and save results to query results
        :return:
        """

        corpus, startYear, endYear, smoothing = 'eng_2012', 1800, 2008, 1
        printHelp, caseInsensitive, allData = False, False, False
        toSave, toPrint, toPlot = True, True, False

        for sense in self.data:
            # Make query always with 12 bigrams because it seems like max amount

            bigrams_not_in_cache = self.get_query_bigrams_not_in_cache(sense['query_bigrams'])

            bigrams_chunked = chunks(bigrams_not_in_cache, 12)

            for bigram_chunk in bigrams_chunked:
                query = self.create_query_string(bigram_chunk)
                print("Querying with ngrams %s" % (query))
                url, urlquery, df = self.getNgrams(query, corpus, startYear, endYear, smoothing, caseInsensitive)
                sense['query_results'] = pd.concat([sense['query_results'], df])


            if self.use_wildcards:
                # Somehow same chunks must be taken again to make this work, idk why...
                bigrams_not_in_cache2 = self.get_query_bigrams_not_in_cache(sense['query_bigrams'],wildcard=True)

                bigrams_chunked2 = chunks(bigrams_not_in_cache2, 12)
                for bigram_chunk2 in bigrams_chunked2:
                    query = self.create_query_string(bigram_chunk2, True)
                    print("Querying with ngrams %s" % (query))
                    url, urlquery, df = self.getNgrams(query, corpus, startYear, endYear, smoothing, caseInsensitive)
                    sense['query_results'] = pd.concat([sense['query_results'], df])

    def create_query_string(self, bigrams, wildcard=False):
        """
        Return query string for query usage
        :param bigrams: List of bigram tuples to be checked
        :param wildcard: Wheter or not wildcard is used
        :return: Query string ready to be used for query to Google Ngram Viewer
        """
        if wildcard == False:
            query = bigrams[0][0] + " " + bigrams[0][1]

            for bigram in bigrams[1:]:
                query = query + "," + bigram[0] + " " + bigram[1]

            return query

        else:
            query = bigrams[0][0] + " * " + bigrams[0][1]

            for bigram in bigrams[1:]:
                query = query + "," + bigram[0] + " * " + bigram[1]

            return query



    def analyze(self):
        """
        Score every sense based on query and/or cache data
        :return:
        """

        for sense in self.data:
            #Modify some column names because Google Ngram Viewer breaks special marks
            modifiednames = {}
            for column in sense['query_results']:
                column_new = column.replace(" - ", "-")
                column_new = column_new.replace("&#39;", "'")

                #Crude way to solve this
                if len(column_new.split()) > 3:
                    column_new = column_new.replace(" 's", "'s")

                if len(column_new.split()) > 3:
                    column_new = column_new.replace("' s", "'s")

                if len(column_new.split()) > 3:
                    column_new = column_new.replace(" 's", "'s")

                # Remove dot spaces crudely
                if len(column_new.split()) > 3:
                    column_new = column_new.replace(" .", ".")

                # Remove slash spaces rudely
                if len(column_new.split()) > 3:
                    column_new = column_new.replace(" / ", "/")

                if column != column_new:
                    modifiednames[column] = column_new
                    print("Column %s will be replaced with name %s" % (column, column_new))


            if len(modifiednames.keys()) > 0:
                sense['query_results'].rename(columns=modifiednames, inplace=True)

            column_scores = {}

            for column in sense['query_results']:
                if (column != 'year'):
                    if '*' in column or (2 == len(column.split())):
                        column_scores[column] = 0

            # If only 1 ngram is found with wildcard query, it requires special calculations because returned data is different

            additional_wildcard_columns = []
            additional_wildcard_columns_lookup_dict = {}

            for column in sense['query_results']:
                if (column != 'year'):
                    if (3 == len(column.split())) and ('*' not in column):
                        found = False
                        column_checking_words = column.split()

                        for column_ready in column_scores.keys():
                            column_ready_words = column_ready.split()

                            if len(column_ready_words) == 2:
                                continue

                            if (column_ready_words[0] == column_checking_words[0]) and (column_ready_words[2] == column_checking_words[2]):
                                found = True
                                break

                        if not found:
                            wc_ngram = column_checking_words[0] + ' * ' + column_checking_words[2]
                            additional_wildcard_columns.append(wc_ngram)
                            additional_wildcard_columns_lookup_dict[column] = wc_ngram


            for awc in additional_wildcard_columns:
                column_scores[awc] = 0

            for index, row in sense['query_results'].iterrows():
                for column in sense['query_results']:
                    if (column != 'year'):
                        if (len(column.split()) == 3) and ('*' not in column):
                            if column not in additional_wildcard_columns_lookup_dict.keys():
                                continue

                        add_score = float(row[column]) * 0.01 * float(self.total_word_counts[str(int(row['year']))])

                        if math.isnan(add_score):
                            continue

                        if column in additional_wildcard_columns_lookup_dict.keys():
                            realcolumn = additional_wildcard_columns_lookup_dict[column]
                            column_scores[realcolumn] += add_score
                        else:
                            column_scores[column] += add_score


            # Retrieving cache data
            cache_data = {}

            if self.use_wildcards:
                cache_data = self.get_bigram_data_existing_in_cache(sense['query_bigrams'],wildcard=True)
            else:
                cache_data = self.get_bigram_data_existing_in_cache(sense['query_bigrams'])

            for ngram, score in column_scores.items():
                insert_cache(ngram, score)


            for ngram, value in cache_data.items():
                column_scores[ngram] = value

            # Detect empty query results and mark them zero to cache
            empty_queries = []
            all_queries = self.create_query_string(sense['query_bigrams']).split(",")

            # Add also wildcards if selected
            if self.use_wildcards:
                all_queries.extend(self.create_query_string(sense['query_bigrams'],True).split(","))

            for q in all_queries:
                if q in column_scores.keys():
                    continue

                empty_queries.append(q)
                insert_cache(q, 0)

            sum_score = 0
            for ngram, score in column_scores.items():
                sum_score += score

            division_count = len(column_scores.keys()) + len(empty_queries)

            if division_count == 0:
                sense['score'] = 0
            else:
                sense['score'] = sum_score / division_count

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

        retry_wait_time = 20

        while True:
            try:
                req = requests.get('http://books.google.com/ngrams/graph', params=params)
            except Exception:
                # Wait minute for connection to repair
                print("Connection error, waiting 60 seconds")
                sleep(60)
                continue

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

            if req.status_code != 200:
                retry_wait_time += 1
                print("Response %s received, waiting %s seconds" % (req.status_code, retry_wait_time))
                sleep(retry_wait_time)

        return req.url, params['content'], df
