import csv
import sys
import operator
from collections import OrderedDict
import re
import progressbar
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


N = 18000

def common_words(filename):
    """
    gets most common words for real and fake news
    :param filename:
    :return:
    """
    FN_words = {}
    RN_words = {}
    corpus = []
    with open(filename, newline="", encoding="utf8") as infile:
        reader = csv.reader(infile, delimiter=',')
        bar = progressbar.ProgressBar()
        for row in bar(reader):
            if reader.line_num > 1:
                corpus.append(row[3])

    # get freq vectorizor
    # NEW STUFF
    vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words="english", max_features=2750)
    vectorizer.fit_transform(corpus)

    return  vectorizer


def author_data(filename):
    """
    get the total
    :param filename:
    :return:
    """
    auth_dict = OrderedDict()
    with open(filename, newline="", encoding="utf8") as infile:
        reader = csv.reader(infile, delimiter=',')
        bar = progressbar.ProgressBar()
        for row in bar(reader):
            if reader.line_num > 1:
                auth_data = row[2]
                if auth_data not in auth_dict:
                    auth_dict[auth_data] = 0
    return auth_dict


def parse(filename):
    """
    parses data from csv
    :param filename:
    :return:
    """

    #Ideas
    #List of fake news topics
    #list of aggressive language commonly used in fake news
    #Grammar

    # Set containing key words
    FN_figures = {"russia":0, "russian":0, "wikileaks":0, "comey":0, "donald":0, "trump":0, "melania":0, "jared":0, "kushner":0,
                      "putin":0, "north":0, "korea":0, "clinton":0, "hicks":0, "flynn":0, " pope":0, "francis":0, "nra":0, "!":0,
                  "mueller":0, "hillary":0, "obama":0, "guns":0, "our":0, "crooked":0, "coal":0, "steve":0, "bannon":0,
                  "emails":0, "take":0, "breitbart":0, "make":0, "america":0, "great":0, "again":0, "power":0,
                  "jew":0, "jewish":0, "black":0, "inner":0,"white":0, "city":0, "race":0, "war":0, "bad":0, "conspiracy":0,
                  "media":0, "liberal":0, "benghazi":0, "pig":0, "woman":0, "republic":0, "cia":0, "organization":0,
                  "bush":0}

    FN_figures = OrderedDict(sorted(FN_figures.items(), key=lambda t: t[0]))
    #top_20_FN, top_20_RN, vectorizer = common_words(filename)
    vectorizer = common_words(filename)

    # get author data
    auth_dict = author_data(filename)


    with open(filename, newline='', encoding="utf8") as infile:
        reader = csv.reader(infile, delimiter=',')
        data = []
        bar = progressbar.ProgressBar()
        i = 0
        for row in bar(reader):
            i += 1
            if i> N:
                break
            example = []
            if reader.line_num>1:
                title_data = row[1].split(" ")
                author = row[2]
                text_data = row[3].split(" ")
                label = row[4]
                # Parse the data from the title
                for title in title_data:
                    Num_Caps = sum(1 for c in title if c.isupper())
                    Num_excalmation_points = title.count("!")
                    Num_Question_marks = title.count("?")
                    Fig_det = 0

                    # get binary representations of words as ordered dict
                    title_dict = OrderedDict()
                    text_dict = OrderedDict()
                    # GET ORDERED DICT OF ALL OF THE MANUALLY GENERATED WORDS
                    for item in FN_figures.keys():
                        title_dict[item] = FN_figures[item]
                        text_dict[item] = FN_figures[item]
                    title_len = len(title) + 1

                    """# get copy ordered dictionaries of common words
                    for key in top_RN.keys():
                        RN_dict[key] = 0
                    for key in top_FN.keys():
                        FN_dict[key] = 0
                    """
                    for word in title:
                        if word.lower() in FN_figures:
                            Fig_det += 1
                            title_dict[word.lower()]= 1 #/title_len
                    # change to fraction of title that are key words
                    Fig_det /= len(title)+1

                copy_auth_dict = OrderedDict()
                # get copy ordered dictionaries of authors
                for key in auth_dict.keys():
                    copy_auth_dict[key] = 0
                copy_auth_dict[author] = 1


                # set up example
                #####################################
                # NEW SHIT
                # http://scikit-learn.org/stable/modules/feature_extraction.html
                # look there for deets
                arr = vectorizer.transform([row[3]]).toarray()
                transformer = TfidfTransformer(smooth_idf=False)
                #tfidf = transformer.fit_transform(arr).toarray()
                farr = arr.flatten()
                #farr = tfidf.flatten()
                larr = list(farr)
                example.extend(larr)
                #############################################


                #example.extend(text_dict.values())
                example.extend( title_dict.values())
                #example.extend(RN_dict.values())
                #example.extend(FN_dict.values())
                example.extend(copy_auth_dict.values())

                #example.append(title_len)
                #example.append(len_text)
                example.extend([Num_Caps, Num_excalmation_points, Num_Question_marks, Fig_det, label])#Fig_text,
                                #CM_RN_text, CM_FN_text,  label])
                data.append(example)
    return data


if __name__ == "__main__":

    parse("kaggle_data.csv")