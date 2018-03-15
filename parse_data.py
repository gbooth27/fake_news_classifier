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

    # Set containing key words
    FN_figures = {"Russia", "Russian", "WikiLeaks", "Comey", "Donald", "Trump", "Melania", "Jared", "Kushner",
                      "Putin", "North", "Korea", "Clinton", "Hicks", "Flynn", " Pope", "Francis", "NRA"}

    with open(filename, newline='') as infile:
        reader = csv.reader(infile, delimiter=',')
        data = []
        for row in reader:
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
                    for word in title:
                        if word in FN_figures:
                            Fig_det += 1
                    # change to fraction of title that are key words
                    Fig_det /= len(title)+1


                len_text = len(text_data)+1
                Fig_text = 0
                for word in text_data:
                    #Find Language set
                    if word in FN_figures:
                        Fig_text +=1
                Fig_text /= len_text


                data.append([Num_Caps, Num_excalmation_points, Num_Question_marks, Fig_det, Fig_text, label])
    return data


if __name__ == "__main__":

    parse("kaggle_data.csv")