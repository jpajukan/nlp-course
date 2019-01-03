import csv
import os
import wikify

def main():
    try:
        stopwords = set(line.strip() for line in open('stopwords.txt'))
    except:
        stopwords = {}
    replacetable = dict.fromkeys(map(ord, ",\n"), None) # characters to remove
    with open("results.csv", "a") as r:
        r.write("corpus" + "," + "word to dissambiguate" + "," + "result" + "\n")
    with open("../testing/combined/testfile_all_blocks_combined_and_cleaned.csv", "r") as f:
        rubbish = f.readline() #read the first line of the data to discard header
        for line in f.readlines():
            corpus,word = line.strip("\n").split(",")
            wikify.wikify(corpus, word.lower(), stopwords)
            with open("output.txt", "r") as o:
                result = o.read()
                result = result.translate(replacetable) #removes the commas from the result
            with open("results.csv", "a") as r:
                r.write(corpus + "," + word + "," + result + "\n")
            with open("results_readable.txt", "a") as r:
                r.write("Corpus: " + corpus + "\n\n" + "Word: " + word + "\n\n" + "The result: " + result + "\n******************************************\n")

if __name__ == "__main__":
    main()
