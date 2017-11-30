
from os                 import listdir
from os.path            import isfile, join
import TagExtractingFuncts

def get_files(path):
    #gets the file paths to the training data
    files = [f for f in listdir(path) if isfile(join(path, f))]
    try :
        del( files[files.index( '.DS_Store' )] )
    except :
        pass
    return files

def read_file(path, file):
    #reads all the text out of a file in a string object
    file_handle = open( join(path, file), 'r' )
    data = file_handle.read()
    file_handle.close()
    return data

def read_wiki(file):
    file = open(file, "r")

    lines = []

    for line in file:
        lines.append(line.replace("\n",""))

    return lines

def read_all_lines(file):
    
    file = open(file, "r")

    lines = []
    
    for line in file:
        lines.append(TagExtractingFuncts.lose_tags(line))
    return lines
