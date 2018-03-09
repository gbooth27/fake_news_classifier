import csv
import sys
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

    FN_figures = ["Russia", "Russian", "WikiLeaks", "Comey", "Donald Trump", "Melania Trump", "Jared Kushner", "Putin", "North Korea", "Clinton", "Hicks", "Flynn", " Pope Francis", "NRA"]

    with open(filename, newline='') as infile:
        reader = csv.reader(infile, delimiter=',')
        for row in reader:
            if reader.line_num>1:
                title_data = row[1]
                author_data = row[2]
                text_data = row[3]

        for title in title_data:
            Num_Caps = sum(1 for c in title if c.isupper())
            Num_excalmation_points = title.count("!")
            Num_Question_marks = title.count("?")
            if any(word in title for word in FN_figures):
                Fig_det = 1

        for text in text_data:
             #Find Language set


    return


if __name__ == "__main__":

    parse("kaggle_data.csv")