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
    FN_figures = {"Russia":0, "Russian":0, "WikiLeaks":0, "Comey":0, "Donald":0, "Trump":0, "Melania":0, "Jared":0, "Kushner":0,
                      "Putin":0, "North":0, "Korea":0, "Clinton":0, "Hicks":0, "Flynn":0, " Pope":0, "Francis":0, "NRA":0, "!":0,
                  "Mueller":0, "Hillary":0, "Obama":0, "guns":0, "our":0, "crooked":0, "coal":0}
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

                    # get binary representations of words
                    title_dict = OrderedDict()
                    text_dict = OrderedDict()
                    for item in FN_figures.keys():
                        title_dict[item] = FN_figures[item]
                        text_dict[item] = FN_figures[item]
                    title_len = len(title) + 1
                    for word in title:
                        if word in FN_figures:
                            Fig_det += 1
                            title_dict[word]+= 1 /title_len
                    # change to fraction of title that are key words
                    Fig_det /= len(title)+1


                len_text = len(text_data)+1
                Fig_text = 0
                for word in text_data:
                    #Find Language set
                    if word in FN_figures:
                        Fig_text +=1
                        text_dict[word]+= 1/len_text
                Fig_text /= len_text

                # set up example
                example.extend(text_dict.values())
                example.extend( title_dict.values())
                example.extend([Num_Caps, Num_excalmation_points, Num_Question_marks, Fig_det, Fig_text, label])
                data.append(example)
    return data


if __name__ == "__main__":

    parse("kaggle_data.csv")