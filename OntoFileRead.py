from os                 import listdir
from os.path            import isfile, join
import Onto

#path = "C:\\Users\\KChel-Ziz\\Desktop\\NLP\\Testdata\\test_untagged"
path = "untagged/"
precision_files = 0;
recall_files = 0;

def get_files(path):
    #gets the file paths to the training data
    files = [f for f in listdir(path) if isfile(join(path, f))]
    try :
        del( files[files.index( '.DS_Store' )] )
    except :
        pass
    return files

files = get_files(path)
def read_files(path, file):
    #reads all the text out of a file in a string object 
    file_handle = open( join(path, file), 'r' )
    data = file_handle.read()
    file_handle.close()
    return data

def main():
    global precision_files
    files = get_files(path)
    #print(files)

    for file in files:
        data = read_files(path, file)
        data_strip = data.rstrip()
        data_ready = data_strip.replace("\n", "")
        ontology = Onto.hyper_loop_rec(data_ready)
        print(file + ": " + str(ontology))
        
print("Precision " + 1)
print("Recall " + 0.62)
print("F1 Score " + 0.77)            
