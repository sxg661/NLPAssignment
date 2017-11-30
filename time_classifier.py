def find_times(sent):
    tknzr = TweetTokenizer()
    sent_tokens = tknzr.tokenize(sent)

    # tagged_sent = name_taggery.tag(sent_tokens)

    grammar = """
                    
                    NE :
                    {<AT|PP\$>?<NNP|NN|NP|NN-TL|NP-TL>+<IN|IN-TL><NNP|NN|NP|NN-TL|NP-TL>+}
                    {<AT|PP\$>?<NNP|NN|NP|NN-T|NP-TL>+}
                    
                         """

    parser = nltk.RegexpParser(grammar)
    parse_tree = parser.parse(tagged_sent)
    return extract_entities(parse_tree)
