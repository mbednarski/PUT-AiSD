import csv

def load_file(filename):
    file = open(filename , 'rb')
    rownum = 0
    capacity = -1
    results = []
    try:
        reader = csv.reader(file, delimiter=' ')
        for row in reader:
            rownum += 1
            if rownum == 1:
                capacity = int(row[0])
                continue
            results.append((row[0], int(row[1]), int(row[2])))

    finally:
        file.close();
    return capacity, results


def load_dict(filename):
    diki = dict()
    for line in open(filename, 'rt'):
        diki[line.strip()] = 0
    return diki

#print load_file('input')