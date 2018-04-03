import csv
import sys
import operator
from collections import OrderedDict
csv.field_size_limit(sys.maxsize)
import re
from collections import Counter




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
    FN_words = {}
    RN_words = {}
    FN_figures = OrderedDict(sorted(FN_figures.items(), key=lambda t: t[0]))
    top_20_FN = []
    top_20_RN = []

    with open(filename, newline='') as infile:
        reader = csv.reader(infile, delimiter=',')
        data = []
        for row in reader:
            example = []
            if reader.line_num>1:
                title_data = row[1].split(" ")
                author_data = row[2]
                text_data = row[3].split(" ")
                label = row[4]
                # Parse the data from the title

                FN_dict = OrderedDict()
                RN_dict = OrderedDict()

                #most common words in Fake News
                if label == 1:
                    for word in text_data:
                        if word.lower() in FN_words:
                            FN_words[word] += 1
                        else:
                            FN_words[word] = 1
                        sorted_FN_words = sorted(FN_words.items(), key=operator.itemgetter(1))
                        list_FN_words = [i[0] for i in sorted_FN_words]
                    top_20_FN = list_FN_words[:20]


                len_text = len(text_data) + 1
                CM_FN_text = 0
                for word in text_data:
                    # Find Language set
                    if word.lower() in top_20_FN:
                        CM_FN_text += 1
                        FN_dict[word.lower()] = 1  # /len_text
                CM_FN_text /= len_text


                #Most common words in Fake News
                if label == 0:
                    for word in text_data:
                        if word.lower() in RN_words:
                            RN_words[word] += 1
                        else:
                            RN_words[word] = 1
                        sorted_RN_words = sorted(RN_words.items(), key=operator.itemgetter(1))
                        list_RN_words =  [i[0] for i in sorted_RN_words]
                    top_20_RN = list_RN_words[:20]


                len_text = len(text_data) + 1
                CM_RN_text = 0
                for word in text_data:
                    # Find Language set
                    if word.lower() in top_20_RN:
                        CM_RN_text += 1
                    RN_dict[word.lower()] = 1  # /len_text
                CM_RN_text /= len_text






                for title in title_data:
                    Num_Caps = sum(1 for c in title if c.isupper())
                    Num_excalmation_points = title.count("!")
                    Num_Question_marks = title.count("?")
                    Fig_det = 0

                    # get binary representations of words as ordered dict
                    title_dict = OrderedDict()
                    text_dict = OrderedDict()
                    for item in FN_figures.keys():
                        title_dict[item] = FN_figures[item]
                        text_dict[item] = FN_figures[item]
                    title_len = len(title) + 1
                    for word in title:
                        if word.lower() in FN_figures:
                            Fig_det += 1
                            title_dict[word.lower()]= 1 #/title_len
                    # change to fraction of title that are key words
                    Fig_det /= len(title)+1


                len_text = len(text_data)+1
                Fig_text = 0
                for word in text_data:
                    #Find Language set
                    if word.lower() in FN_figures:
                        Fig_text +=1
                        text_dict[word.lower()]= 1#/len_text
                Fig_text /= len_text

                # set up example
                example.extend(text_dict.values())
                example.extend( title_dict.values())
                #example.append(title_len)
                #example.append(len_text)
                example.extend([Num_Caps, Num_excalmation_points, Num_Question_marks, Fig_det, Fig_text, CM_RN_text, CM_FN_text, label])
                data.append(example)
    return data


if __name__ == "__main__":

    parse("kaggle_data.csv")