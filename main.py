import argparse

from googlengramtesting import *

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
    result = wn.synsets("bank")
    for ss in result:
        print(build_contextual_wording(ss))
        print("\n")


    # Test word stuff
    sentence1 = "I like fishing at bank of the river"
    sentence2 = "I loaned money from the bank of the America"

    s1 = prepare_context_sentence(sentence1, "bank")
    s2 = prepare_context_sentence(sentence2, "bank")

    cw = build_contextual_wording(wn.synsets("bank")[0])
    cooccurence_bank(s2)

if __name__ == '__main__':
    main()