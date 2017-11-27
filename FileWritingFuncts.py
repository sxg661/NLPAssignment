import FileReadingFuncts
import TagExtractingFuncts


def createsFiles(tag_names):
    path = "training/"
    
    files = FileReadingFuncts.get_files(path)

    

    for file in files:
        data = FileReadingFuncts.read_file(path, file)
        for  i in range(0, len(tag_names)):
            newMatches  = TagExtractingFuncts.find_tag_matches(tag_names[i], data)
            for match in newMatches
            #THIS FILE IS HALF FINISHED!
            

    return tag_matches
            

def getblank2d(length):
    blank = []
    for i in range(0,length):
        blank.append(

def writeFile(matches, output_file):
    file = open(output_file, w)

    for match in matches:
        file.write(match)

    file.close();

    



