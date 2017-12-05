import FileReadingFuncts
import TagExtractingFuncts
import WikipediaFuncts


def createsFiles(tag_names):

    #reads in the tags
    path = "training/"
    
    files = FileReadingFuncts.get_files(path)

    matches = getblank2d(len(tag_names))

    for file in files:
        data = FileReadingFuncts.read_file(path, file)
        for  i in range(0, len(tag_names)):
            newMatches  = TagExtractingFuncts.find_tag_matches(tag_names[i], data)
            matches[i] = matches[i] + (newMatches)


    #writes the tags to the files
    for i in range(0, len(tag_names)):
        outputFile = "tagFiles/{}.txt".format(tag_names[i])
        writeFile(set(matches[i]), outputFile)

            
def writeWikiFile(tag_name):
    #reads in all the example tags from the tag file
    entities = FileReadingFuncts.read_all_lines("tagFiles/{}.txt".format(tag_name))[:20]

    #gets the words related to these from wikipedia
    words = []
    for entity in entities:
        words = words + WikipediaFuncts.get_words(entity)

    #writes these words to the output file
    output_file = "wiki/{}1.txt".format(tag_name)
    writeFile(words, output_file)
    


def getblank2d(length):
    blank = []
    for i in range(0,length):
        blank.append([])
    return blank


def writeFile(matches, output_file):
    file = open(output_file, "w")

    for match in matches:
        match = match.replace("\n"," ")
        file.write(match + "\n")

    file.close();

    
def writeTaggedFile(data, file):
    output_file = "my_tagged/{}".format(file)

    file = open(output_file,"w")

    file.write(data)

    file.close()


