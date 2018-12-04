import wikipedia, sys
import nltk

#### wikifies the whole input corpus
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
                #print(entity)
                #split_entities = list(set(entity.strip().split(' ')))
                split_entities = entity.split(" ")
                #print(split_entities)
                #tokens = tokenizer.tokenize(split_entities)
                #print(type(entity))
                #print(type(split_entities))
                #print('getting info for: ', entity)
                for i in split_entities:
                    w.write(i+" ")
                    i = i.lower().strip(".,:;'!?=")
                    if i and i not in stopwords:
                        print("##### TOKEN #####: ", i)
                        try:
                            search = wikipedia.search(i)
                            if search:
                                page = wikipedia.page(search[0])
                                if page.url:
                                    w.write('<'+page.url+'> ')
                            # get the outgoing links from this page
                            #entity_links[i] = page.links
                            # get the text on this page
                            #entity_text[i] = page.content
                        except Exception as e:
                            #print(e)
                            continue
                




main()
