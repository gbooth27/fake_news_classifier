import csv
import sys
import operator
from collections import OrderedDict
csv.field_size_limit(sys.maxsize)
import re
import progressbar
from collections import Counter

N = 18000

def common_words(filename):
    """
    gets most common words for real and fake news
    :param filename:
    :return:
    """
    FN_words = {}
    RN_words = {}
    with open(filename, newline="") as infile:
        reader = csv.reader(infile, delimiter=',')
        bar = progressbar.ProgressBar()
        i = 0
        for row in bar(reader):
            i += 1
            if i > N//2:
                break

            if reader.line_num > 1:
                text_data = row[3].split(" ")
                label = row[4]
                # most common words in Fake News
                if label == '1':
                    for word in text_data:
                        if word.lower() in FN_words:
                            FN_words[word.lower()] += 1
                        else:
                            FN_words[word.lower()] = 1
                # Most common words in Real News
                else:
                    for word in text_data:
                        if word.lower() in RN_words:
                            RN_words[word.lower()] += 1
                        else:
                            RN_words.update({word.lower(): 1})
    # get the top twenty of each
    sorted_RN_words = sorted(list(RN_words.items()), key=lambda x: x[1])
    top_20_RN = sorted_RN_words[:40]
    sorted_FN_words = sorted(list(FN_words.items()), key=lambda x: x[1])
    top_20_FN = sorted_FN_words[:40]

    return top_20_FN, top_20_RN


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
    top_20_FN, top_20_RN = common_words(filename)
    top_FN = OrderedDict(top_20_FN)
    top_RN = OrderedDict(top_20_RN)


    with open(filename, newline='') as infile:
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
                author_data = row[2]
                text_data = row[3].split(" ")
                label = row[4]
                # Parse the data from the title

                FN_dict = OrderedDict()
                RN_dict = OrderedDict()

                len_text = len(text_data) + 1
                CM_FN_text = 0
                for word in text_data:
                    # Find Language set
                    if word.lower() in FN_dict:
                        CM_FN_text += 1
                        #FN_dict[word.lower()] = 1  # /len_text
                CM_FN_text /= len_text



                len_text = len(text_data) + 1
                CM_RN_text = 0
                for word in text_data:
                    # Find Language set
                    if word.lower() in RN_dict:
                        CM_RN_text += 1
                    #RN_dict[word.lower()] = 1  # /len_text
                CM_RN_text /= len_text


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

                    # get copy ordered dictionaries of common words
                    for key in top_RN.keys():
                        RN_dict[key] = 0
                    for key in top_FN.keys():
                        FN_dict[key] = 0

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
                        text_dict[word.lower()] = 1000/len_text
                    # check if common RN dict
                    if word.lower() in RN_dict:
                        RN_dict[word.lower()] = 1000/len_text

                    # check if common FN dict
                    if word.lower() in FN_dict:
                        FN_dict[word.lower()] = 1000/len_text

                Fig_text /= len_text

                # set up example
                example.extend(text_dict.values())
                example.extend( title_dict.values())
                example.extend(RN_dict.values())
                example.extend(FN_dict.values())

                #example.append(title_len)
                #example.append(len_text)
                example.extend([Num_Caps, Num_excalmation_points, Num_Question_marks, Fig_det, Fig_text,
                                CM_RN_text, CM_FN_text,  label])
                data.append(example)
    return data


if __name__ == "__main__":

    parse("kaggle_data.csv")