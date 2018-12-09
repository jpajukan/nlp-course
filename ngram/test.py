from google_ngram_algorithm import GoogleNgramAlgorithm

def main():

    # Not very good test word stuff. Try different ones


    sentence = "I like to tie knots in rope"
    target_word = "tie"

    sentence = "I loaned money from bank to buy new apartment"
    target_word = "bank"


    # Algorithm seems to be working nicely with this one (but might just be coincidence)
    sentence = "We went to see the famous play at the theater"
    target_word = "play"

    # Not producing good with this one
    sentence = "Most successful football team play at the stadium tonight"
    target_word = "play"

    #ngra = GoogleNgramAlgorithm(target_word, sentence, 6, 2)
    ngra = GoogleNgramAlgorithm(target_word, sentence)

    ngra.prepare()
    ngra.query_google_ngram()

    ngra.analyze()

    ngra.print_results()

    print(ngra.get_all_results())

if __name__ == '__main__':
    main()