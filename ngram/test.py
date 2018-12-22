from google_ngram_algorithm import GoogleNgramAlgorithm
import sys
import csv



def main():

    usage = 'test.py <csv input file> <csv output file>'

    if len(sys.argv) < 3:
        print(usage)
        sys.exit(1)

    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    with open(inputfile, encoding="utf-8") as csvInputFile, open(outputfile, 'w') as csvOutputFile:
        csv_reader = csv.reader(csvInputFile, delimiter=',')
        csv_writer = csv.writer(csvOutputFile, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
            else:
                wordAndSentence = "Word: ", row[1], "Sentence: ", row[0]
                print(wordAndSentence)
                csv_writer.writerow(wordAndSentence)

                ngra = GoogleNgramAlgorithm(row[1], row[0], 2, 2)

                ngra.prepare()
                ngra.query_google_ngram()

                ngra.analyze()

                #ngra.print_results()
                #print(ngra.get_all_results())
                results = ngra.get_all_results()
                print(results)
                for outputRow in results:
                    print(str(results[0][0]), ",", str(results[0][2]))
                    csv_writer.writerow(outputRow)
                csv_writer.writerow("\n\n")
            line_count += 1

        print(f'Processed {line_count} lines.')

    # Not very good test word stuff. Try different ones

    #sentence = "I like to tie knots in rope"
    #target_word = "tie"

    #sentence = "I loaned money from bank to buy new apartment"
    #target_word = "bank"


    # Algorithm seems to be working nicely with this one (but might just be coincidence)
    #sentence = "We went to see the famous play at the theater"
    #target_word = "play"

    # Not producing good with this one
    #sentence = "Most successful football team play at the stadium tonight"
    #target_word = "play"

    #ngra = GoogleNgramAlgorithm(target_word, sentence, 6, 2)


if __name__ == '__main__':
    main()