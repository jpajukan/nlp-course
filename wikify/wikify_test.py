import wikify

def main():
    try:
        stopwords = set(line.strip() for line in open('stopwords.txt'))
    except:
        stopwords = {}
    with open("results.csv", "a") as r:
        r.write("corpus" + "," + "word to dissambiguate" + "," + "result" + "\n")
    with open("results_for_validation.csv", "a") as r:
        r.write("corpus" + "," + "word to dissambiguate" + "," + "result" + "\n")
    with open("../testing/combined/testfile_all_blocks_combined_and_cleaned.csv", "r") as f:
        rubbish = f.readline() #read the first line of the data to discard header
        for line in f.readlines():
            corpus,word = line.strip("\n").split(",")
            wikify.wikify(corpus, word.lower(), stopwords)
            with open("output.txt", "r") as o:
                result = o.read()
                result_split = result.split(", ") #this to enable the usage of only url (index 1)
            with open("results_for_validation.csv", "a") as r:
                r.write(word + ", " + result_split[0] + ", " + result_split[1] + "\n")
            with open("results.csv", "a") as r:
                r.write(corpus + "," + word + "," + result + "\n")
            with open("results_readable.txt", "a") as r:
                r.write("Corpus: " + corpus + "\n\n" + "Word: " + word + "\n\n" + "The result: " + result + "\n******************************************\n")

if __name__ == "__main__":
    main()
