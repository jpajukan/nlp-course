import csv
import os
import wikify

def main():
    try:
        stopwords = set(line.strip() for line in open('stopwords.txt'))
    except:
        stopwords = {}
    replacetable = dict.fromkeys(map(ord, ","), None) # characters to remove
    with open("results.csv", "a") as r:
        r.write("corpus" + "," + "word to dissambiguate" + "," + "result" + "\n")
    with open("../testing/testfile_all_tests.csv", "r") as f:
        rubbish = f.readline() #read the first line of the data to discard header
        for line in f.readlines():
            corpus,word = line.strip("\n").split(",")
            wikify.wikify(corpus, word.lower(), stopwords)
            with open("output.txt", "r") as o:
                result = o.read()
                result = result.translate(replacetable) #removes the commas from the result
            with open("results.csv", "a") as r:
                r.write(corpus + "," + word + "," + result + "\n")

if __name__ == "__main__":
    main()
