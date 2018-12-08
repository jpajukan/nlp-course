import wikipedia, sys
import nltk

#### (disambiguates) wikifies the given word in regard of the given corpus
def main():
    usage = 'extract_links.py <infile>'
    
    if len(sys.argv) < 2:
        print(usage)
        sys.exit(1)


    surface_file = sys.argv[1]
    stopwords = set(line.strip() for line in open('stopwords.txt'))
    #with open('stopwords.txt') as f:
    #    for word in f.readlines():
    #        print(word)
    #        stopwords.update(word)

    #print(stopwords)
    #input()
    entity_links = {}
    entity_text = {}
    #tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    with open(surface_file) as f:
        with open("output.txt", "w") as w:
            for entity in f.readlines():
                split_entities = entity.strip().split(". ")
                for i in split_entities:
                    split_words = i.split(" ")
                    set_words = set(split_words)
                    for j in split_words:
                        #w.write(i+" ")
                        #i = i.lower().strip(".,:;'!?=")
                        if j and j.lower() not in stopwords:
                            print("##### TOKEN #####: ", j)
                            try:
                                search = wikipedia.search(j)
                                if search:
                                    page = wikipedia.page(search[0])
                                    if page.url:
                                        links=set(page.links)
                                        w.write('<'+page.url+'> ')
                                # get the outgoing links from this page
                                #entity_links[i] = page.links
                                # get the text on this page
                                #entity_text[i] = page.content
                            except Exception as e:
                                #print(e)
                                continue
                




main()
