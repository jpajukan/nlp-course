import wikipedia, sys
import nltk
import difflib

#### (disambiguates) wikifies the given word in regard of the given corpus
def main():
    usage = 'wikify_3.py <string for context> <word to disambiguate>'
    
    if len(sys.argv) < 3:
        print(usage)
        sys.exit(1)


    corpus = sys.argv[1]
    word_dissamb = sys.argv[2].lower()
    stopwords = set(line.strip() for line in open('stopwords.txt'))
    #with open(surface_file) as f:
    with open("output.txt", "w") as w:
        #entity = f.read()
        #print(entity)
        entities = list(set(corpus.strip("\" '!?,:;").lower().split(" ")) - stopwords)
        try:
            results = wikipedia.search(word_dissamb)
        except wikipedia.exceptions.DisambiguationError as e:
            results = e.options

        max_percent=0
        max_percent_index=0
        for i, result in enumerate(results):
            try:
                page = wikipedia.page(result)
                links = list(set(page.summary.strip("\" '!?,:;").lower().split(" ")) - stopwords)
                title = page.title.lower()
            except:
                print("Skipped: ", result)
                continue

            percent=(difflib.SequenceMatcher(a=entities, b=links).ratio() + difflib.SequenceMatcher(a=word_dissamb, b=title).ratio())*(50)
            #percent=(difflib.SequenceMatcher(a=entities, b=links).ratio() + 0.5 * difflib.SequenceMatcher(a=word_dissamb, b=title).ratio())*(100/1.5)
            print("The result: ", result, round(percent, 3))

            if percent > max_percent:
                max_percent=percent
                max_percent_index=i
        final_result = wikipedia.page(results[max_percent_index])
        w.write(final_result.title + '\n' + final_result.url + '\n' + final_result.summary)
        print("The best match in this context was ", final_result.title, ' ', final_result.url)


main()
