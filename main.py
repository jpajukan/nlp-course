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


if __name__ == '__main__':
    main()