from google_ngram_algorithm import GoogleNgramAlgorithm


def main():
    sentence = "Almost all the music was composed by the trio"
    word = "composed"

    #sentence = "They will consider supporting anticolonialist and nationalist movements. The Intelligence Community believes their area of greatest interest will be Southeast Asia although they probably will not insert Chinese Communist regular troops"
    #word = "insert"

    sentence = "The SS ''Manhattan'' was an oil tanker that became the first commercial ship to cross the Northwest Passage in 1969. For this voyage she was refitted with an icebreaker bow"
    word = "tanker"

    #sentence = "Thirty years later in October 1881 a violent storm caused serious damage to the Cathedral's 240 ft. spire. Canon Beesley then the administrator succeeded in raising funds for repairs to the spire and generally refurbishing the fabric of the building"
    #word = "funds"

    #sentence = "As far as organization and management the report described the structure of the Directorate of Plans (i.e. the clandestine service) as too complex and in need of simplification"
    #word = "complex"

    # Ei tunnista adjektiivia complex ollenkaan! Kun ei se saa luotua niille sense wordingiä. Vähän parempi tulos kun antaa target wordin olla sense wordeissa mukana

    ngra = GoogleNgramAlgorithm(word, sentence, 6, 6, use_wildcards=True)

    ngra.prepare()
    ngra.query_google_ngram()

    ngra.analyze()

    ngra.print_results()
    print(ngra.get_all_results())


if __name__ == '__main__':
    main()