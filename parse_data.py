import csv
import sys
csv.field_size_limit(sys.maxsize)


def parse(filename):
    """
    parses data from csv
    :param filename:
    :return:
    """
    data = []
    with open(filename, newline='') as infile:
        reader = csv.reader(infile, delimiter=',')
        for row in reader:
            if reader.line_num>1:
                example = [row[2], int(row[-1])]
                data.append(example)
    return data




if __name__ == "__main__":
    parse("kaggle_data.csv")