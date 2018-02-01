import TagExtractingFuncts
import FileReadingFuncts


def get_all_tags(path, file, tag_name):
    #reads in the file:
    data = FileReadingFuncts.read_file(path, file)

    #finds all the matches
    tagged_matches = TagExtractingFuncts. find_tag_matches(tag_name, data)

    #removes the tags from every match
    untagged_matches = []
    for match in tagged_matches:
        match = match.replace(".","")
        untagged_matches.append(TagExtractingFuncts.get_rid_of_tags(match))

    return untagged_matches


#this class stores all information about score for a certain tag,
#and performs any necessary calculations
class TagScoreCalculator:
    def __init__(self, tag_name):
        self.tag_name = tag_name
        self.test_tags = []
        self.my_tags = []
        self.recall = None
        self.precision = None
        self.f1Score = None

    @staticmethod
    def create_tag_dict(tag_names):
        tag_dict = {}
        for tag_name in tag_names:
            tag_dict[tag_name] = TagScoreCalculator(tag_name)
        return tag_dict

    def add_tags(self,test_tags,my_tags):
        self.test_tags = self.test_tags + test_tags
        self.my_tags = self.my_tags + my_tags

    def calculate_scores(self):
        #by putting them into sets I remove duplicates
        #and can use set operations to make calcluations easier
        test_tags_set = set(self.test_tags)
        my_tags_set = set(self.my_tags)

        

        #things that are classified and that were meant to be classified
        true_positives = my_tags_set.intersection(test_tags_set)

        self.precision = len(true_positives) / len(my_tags_set)
        self.recall = len(true_positives) / len(test_tags_set)
        try:
            self.f1Score = 2 * ( (self.precision * self.recall) / (self.precision + self.recall) )
        except(ZeroDivisionError):
            self.f1Score = 0

    def print(self):
        print("---------------------------------------------")
        print(self.tag_name)
        print("---------------------------------------------")
        print("Precision   :   {}".format(self.precision))
        print("Recall      :   {}".format(self.recall))
        print("F1 Score    :   {}".format(self.f1Score))
        
        
        

def read_in_tags():
    tag_names = ["sentence","paragraph","speaker","location","etime","stime"]

    #creates a dictionary in which to store all the tag scores
    tag_scores = TagScoreCalculator.create_tag_dict(tag_names)

    #(I only have to read in the file nams from one directory because
    #they're the same for both)
    for tagFile in FileReadingFuncts.get_files("test_tagged/"):
        for tag_name in tag_names:
            #reads in all the tagged stuff from the tagged files
            test_tags = get_all_tags("test_tagged/",tagFile,tag_name)
            my_tags = get_all_tags("my_tagged/",tagFile,tag_name)

            #adds the tags I read in into my tag_score dictionary
            tag_scores[tag_name].add_tags(test_tags,my_tags)

    return tag_scores


    
            
if __name__ == '__main__':
    tag_scores = read_in_tags()

    for key in tag_scores.keys():
        tag_scores[key].calculate_scores()
        tag_scores[key].print()

    print("---------------------------------------------")







    
