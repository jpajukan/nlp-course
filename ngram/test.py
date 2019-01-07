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

                #ngra = GoogleNgramAlgorithm(row[1], row[0], 2, 2)
                ngra = GoogleNgramAlgorithm(row[1], row[0], 3, 2, use_wildcards=True)
                #ngra = GoogleNgramAlgorithm(row[1], row[0], 4, 2, use_wildcards=True)
                #ngra = GoogleNgramAlgorithm(row[1], row[0], 4, 3, use_wildcards=True)
                #ngra = GoogleNgramAlgorithm(row[1], row[0], 10, 12, use_wildcards=True)
                #ngra = GoogleNgramAlgorithm(row[1], row[0], 12, 12, use_wildcards=True)
                ngra.prepare()
                ngra.query_google_ngram()

                ngra.analyze()

                results = ngra.get_all_results()
                print(results)
                for outputRow in results:
                    print(str(results[0][0]), ",", str(results[0][2]))
                    csv_writer.writerow(outputRow)
                csv_writer.writerow("\n\n")
            line_count += 1

        print(f'Processed {line_count} lines.')


if __name__ == '__main__':
    main()