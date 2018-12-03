import argparse

from googlengramtesting import *

from encopyngram import *

def main():
    parser = argparse.ArgumentParser(description='Calculate something with ngram')

    parser.add_argument('inputword1', help='inputword1 help')

    args = parser.parse_args()

    # Testing google ngram
    #ngram_wiki_example()
    #ngram_cooccurence_example()

    #ngram_example2(args.inputword1)

    #ngram_example_5_gram()

    #modded_cooccurence_function()


    # Testing wordnet stuff for contextual wording
    #result = wn.synsets("bank")
    #for ss in result:
    #    print(build_contextual_wording(ss))
    #    print("\n")


    # Test word stuff
    sentence1 = "I like fishing at bank of the river"
    #sentence2 = "I loaned money from the bank of the America"

    s1 = prepare_context_sentence(sentence1, "bank")
    #s2 = prepare_context_sentence(sentence2, "bank")

    cw = build_contextual_wording(wn.synsets("bank")[0])

    cw2 = build_contextual_wording(wn.synsets("bank")[1])
    print(cw)
    print(cw2)

    #cooccurence_bank(s2)

    #Playing with encopy script

    #runQuery("money bank, money river")

    ##runQuery("river")

    score1 = 0

    score2 = 0

    for sword in s1:
        for con_word in cw:
            test_query = sword + " " + con_word
            print(test_query)
            returned_dataframe = runQuery(test_query + " -return")
            if test_query in returned_dataframe:
                score1 += returned_dataframe[test_query].sum()

            test_query = con_word + " " + sword
            print(test_query)
            returned_dataframe = runQuery(test_query + " -return")
            if test_query in returned_dataframe:
                score1 += returned_dataframe[test_query].sum()

    for sword in s1:
        for con_word in cw2:
            test_query = sword + " " + con_word
            print(test_query)
            returned_dataframe = runQuery(test_query + " -return")
            if test_query in returned_dataframe:
                score2 += returned_dataframe[test_query].sum()

            test_query = con_word + " " + sword
            print(test_query)
            returned_dataframe = runQuery(test_query + " -return")
            if test_query in returned_dataframe:
                score2 += returned_dataframe[test_query].sum()


    print("Score of sense 1 to sentence 1: " + str(score1))
    print("Score of sense 2 to sentence 1: " + str(score2))

if __name__ == '__main__':
    main()