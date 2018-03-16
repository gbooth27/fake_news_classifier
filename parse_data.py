import csv
import sys
from collections import OrderedDict
csv.field_size_limit(sys.maxsize)


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
                  "media":0, "liberal":0, "benghazi":0}
    FN_figures = OrderedDict(sorted(FN_figures.items(), key=lambda t: t[0]))

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
                example.extend([Num_Caps, Num_excalmation_points, Num_Question_marks, Fig_det, Fig_text, label])
                data.append(example)
    return data


if __name__ == "__main__":

    parse("kaggle_data.csv")