import FileReadingFuncts
import TagExtractingFuncts


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

    



