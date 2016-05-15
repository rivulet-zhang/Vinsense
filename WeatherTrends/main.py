import os
import csv
import json
import collections
from operator import itemgetter


def firstdiff(l):

    for idx, val in enumerate(l):
        if idx == 0:
            continue
        if l[idx][3] != l[idx-1][3]:
            return idx
    return len(l)


if __name__ == '__main__':

    #  load all json files
    csvDir = os.path.dirname(os.path.realpath(__file__)) + '\data\csv'
    print(csvDir)

    csv_files = [pos_json for pos_json in os.listdir(csvDir) if pos_json.endswith('.csv')]
    print('number of files:', len(csv_files))

    db = dict()

    for f in csv_files:
        with open(os.path.join(csvDir, f)) as csv_file:
            reader = csv.reader(csv_file)
            data = list(reader)
            # remove header
            data.pop(0)
            # current date format: 2016-01-12
            currentDate = f.split('_')[0]
            # loop each predicted row in the file
            for d in data:
                date = d[0].split('UTC')[0]
                temp = [currentDate, d[1], d[2], d[3]]

                # not valid prediction
                if float(d[1]) < -900:
                    continue

                if date not in db.keys():
                    db[date] = []

                db[date].append(temp)

    # check length of forward days of update
    rst = []
    for key in db:
        goal = db[key]
        firstindex = firstdiff(goal)
        size = len(goal) - firstindex
        # print(goal)
        rst.append(key+'  '+str(size))

    rst = sorted(rst)
    print('\n'.join(rst))

    print(db['2017-01-29'])

    # with open('rst.json', 'w') as outfile:
    #     json.dump(db, outfile, indent=2)

    # calculate temperature difference

    diff = {}
    for key in db:
        goal = db[key]
        accurate = goal[len(goal)-1]
        _diff = []
        for val in goal:
            _diff.append([val[0],
                          float(val[1]) - float(accurate[1]),
                          float(val[2]) - float(accurate[2]),
                          float(val[3]) - float(accurate[3])
                          ])
        diff[key] = _diff

    print(diff['2016-04-20'])
