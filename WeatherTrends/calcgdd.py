import os
import csv, json
from datetime import date

# def firstdiff(l):
#
#     for idx, val in enumerate(l):
#         if idx == 0:
#             continue
#         if l[idx][3] != l[idx-1][3]:
#             return idx
#     return len(l)


def getGdd(temp):
    return temp - 50 if temp > 50 else 0


def avglist(l):
    return sum(l) / len(l)


def calculateGdd(hisTempFile, hisRange, predictTempFolder, predictStart):

    #  load all csv files
    csvDir = os.path.dirname(os.path.realpath(__file__)) + predictTempFolder
    print('dataDir:', csvDir)

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
    # rst = []
    # for key in db:
    #     goal = db[key]
    #     firstindex = firstdiff(goal)
    #     size = len(goal) - firstindex
    #     # print(goal)
    #     rst.append(key+'  '+str(size)+'  '+' '.join(db[key][-1]))
    #
    # rst = sorted(rst)

    # calculate temperature difference

    # diff = {}
    # for key in db:
    #     goal = db[key]
    #     accurate = goal[len(goal)-1]
    #     _diff = []
    #     for val in goal:
    #         _diff.append([val[0],
    #                       float(val[1]) - float(accurate[1]),
    #                       float(val[2]) - float(accurate[2]),
    #                       float(val[3]) - float(accurate[3])
    #                       ])
    #     diff[key] = _diff

    predictData = []
    # output = []
    for key in db:
        predictData.append([key, db[key][-1][3]])
        # output.append(key+" "+predictData[key])

    predictData.sort(key=lambda x: x[0])

    # print data of current year
    # print('\n'.join(','.join(r) for r in predictData))

    # load help file [historical temporal file]
    helpFileDir = os.path.dirname(os.path.realpath(__file__)) + hisTempFile
    print('helpFileDir:', helpFileDir)

    hisData = []
    with open(helpFileDir) as help_file:
        reader = csv.reader(help_file)
        hisData = list(reader)
        hisData = hisData[1:]

    # load season aggregation file
    # seasonFile = os.path.dirname(os.path.realpath(__file__)) + hisSeasonFile
    # print('seasonFile:', seasonFile)

    # season = {}
    # with open(seasonFile) as data_file:
    #     season = json.load(data_file)

    # print(season)

    # gdd_s1 = 0
    # gdd_s2 = 0
    # gdd_s3 = 0
    #
    # temp_s1 = []
    # temp_s2 = []
    # temp_s3 = []

    # calculate gdd

    hisGdd = 0
    hisTemp = []

    for val in hisData:
        date = val[0]
        temp = float(val[1])

        if hisRange[0] <= date <= hisRange[1]:
            hisGdd += getGdd(temp)
            hisTemp.append(temp)
            print(date, temp, getGdd(temp), hisGdd)

    # print('gdd_s1', gdd_s1, 'gdd_s2', gdd_s2, 'gdd_s3', gdd_s3)

    # predict new season

    # specify start date
    # startDate = '2016-03-01'

    startDate = predictStart

    # currSeason = 1
    # gdd = [0, gdd_s1, gdd_s2, gdd_s3]
    # avgtemp_curr = [0,[],[],[]]
    # sum = 0
    # milestone = [startDate]
    # predictedGdd = []

    predictGdd = 0
    predictTemp = []

    predictEnd = 0
    for idx, data in enumerate(predictData):

        if data[0] < startDate:
            continue

        temp = float(data[1])
        predictGdd += getGdd(temp)
        predictTemp.append(temp)
        print(data[0], temp, getGdd(temp), predictGdd)

        if predictGdd >= hisGdd:
            predictEnd = data[0]
            break

    rst = {}
    rst['historical'] = {}
    rst['historical']['dates'] = hisRange
    rst['historical']['gdd'] = hisGdd
    rst['historical']['avgtemp'] = avglist(hisTemp)

    rst['predicted'] = {}
    rst['predicted']['dates'] = [predictStart, predictEnd]
    rst['predicted']['gdd'] = predictGdd
    rst['predicted']['avgtemp'] = avglist(predictTemp)

    return rst


# def calculateGddBackup(hisTempFile, hisSeasonFile, predictTempFolder, predictBudBreakDate):
#
#     #  load all csv files
#     csvDir = os.path.dirname(os.path.realpath(__file__)) + predictTempFolder
#     print('dataDir:', csvDir)
#
#     csv_files = [pos_json for pos_json in os.listdir(csvDir) if pos_json.endswith('.csv')]
#     print('number of files:', len(csv_files))
#
#     db = dict()
#
#     for f in csv_files:
#         with open(os.path.join(csvDir, f)) as csv_file:
#             reader = csv.reader(csv_file)
#             data = list(reader)
#             # remove header
#             data.pop(0)
#             # current date format: 2016-01-12
#             currentDate = f.split('_')[0]
#             # loop each predicted row in the file
#             for d in data:
#                 date = d[0].split('UTC')[0]
#                 temp = [currentDate, d[1], d[2], d[3]]
#
#                 # not valid prediction
#                 if float(d[1]) < -900:
#                     continue
#
#                 if date not in db.keys():
#                     db[date] = []
#
#                 db[date].append(temp)
#
#     # check length of forward days of update
#     # rst = []
#     # for key in db:
#     #     goal = db[key]
#     #     firstindex = firstdiff(goal)
#     #     size = len(goal) - firstindex
#     #     # print(goal)
#     #     rst.append(key+'  '+str(size)+'  '+' '.join(db[key][-1]))
#     #
#     # rst = sorted(rst)
#
#     # calculate temperature difference
#
#     # diff = {}
#     # for key in db:
#     #     goal = db[key]
#     #     accurate = goal[len(goal)-1]
#     #     _diff = []
#     #     for val in goal:
#     #         _diff.append([val[0],
#     #                       float(val[1]) - float(accurate[1]),
#     #                       float(val[2]) - float(accurate[2]),
#     #                       float(val[3]) - float(accurate[3])
#     #                       ])
#     #     diff[key] = _diff
#
#     predictData = []
#     # output = []
#     for key in db:
#         predictData.append([key, db[key][-1][3]])
#         # output.append(key+" "+predictData[key])
#
#     predictData.sort(key=lambda x: x[0])
#
#     # print data of current year
#     # print('\n'.join(','.join(r) for r in predictData))
#
#     # load help file [historical temporal file]
#     helpFileDir = os.path.dirname(os.path.realpath(__file__)) + hisTempFile
#     print('helpFileDir:', helpFileDir)
#
#     hisData = []
#     with open(helpFileDir) as help_file:
#         reader = csv.reader(help_file)
#         hisData = list(reader)
#         hisData = hisData[1:]
#
#     # load season aggregation file
#     seasonFile = os.path.dirname(os.path.realpath(__file__)) + hisSeasonFile
#     print('seasonFile:', seasonFile)
#
#     season = {}
#     with open(seasonFile) as data_file:
#         season = json.load(data_file)
#
#     # print(season)
#
#     gdd_s1 = 0
#     gdd_s2 = 0
#     gdd_s3 = 0
#
#     temp_s1 = []
#     temp_s2 = []
#     temp_s3 = []
#
#     # calculate gdd
#
#     for val in hisData:
#         date = val[0]
#         temp = float(val[1])
#
#         if season['s1'][0] <= date <= season['s1'][1]:
#             gdd_s1 += getGdd(temp)
#             temp_s1.append(temp)
#         if season['s2'][0] <= date <= season['s2'][1]:
#             gdd_s2 += getGdd(temp)
#             temp_s2.append(temp)
#         if season['s3'][0] <= date <= season['s3'][1]:
#             gdd_s3 += getGdd(temp)
#             temp_s3.append(temp)
#
#     # print('gdd_s1', gdd_s1, 'gdd_s2', gdd_s2, 'gdd_s3', gdd_s3)
#
#     # predict new season
#
#     # specify start date
#     # startDate = '2016-03-01'
#     startDate = predictBudBreakDate
#     print("start date of predicted year:", startDate)
#
#     currSeason = 1
#     gdd = [0, gdd_s1, gdd_s2, gdd_s3]
#     avgtemp_curr = [0,[],[],[]]
#     sum = 0
#     milestone = [startDate]
#     predictedGdd = []
#
#     for idx, data in enumerate(predictData):
#         if data[0] < startDate:
#             continue
#         temp = float(data[1])
#         sum += getGdd(temp)
#         avgtemp_curr[currSeason].append(temp);
#
#         if sum >= gdd[currSeason]:
#             milestone.append(data[0])
#             milestone.append(predictData[idx+1][0])
#
#             currSeason += 1
#             predictedGdd.append(int(round(sum)))
#             sum = 0
#             if currSeason > 3:
#                 break
#
#     # print(milestone)
#
#     # check the calculation
#
#     # gdd_s1 = gdd_s2 = gdd_s3 = 0
#     #
#     # for val in predictData:
#     #     date = val[0]
#     #     temp = float(val[1])
#     #
#     #     if '2016-03-01' <= date <= '2016-04-18':
#     #         gdd_s1 += getGdd(temp)
#     #     if '2016-04-19' <= date <= '2016-06-05':
#     #         gdd_s2 += getGdd(temp)
#     #     if '2016-06-06' <= date <= '2016-08-14':
#     #         gdd_s3 += getGdd(temp)
#     #
#     # print('gdd_s1', gdd_s1, 'gdd_s2', gdd_s2, 'gdd_s3', gdd_s3)
#
#     rst = {}
#     rst['historical'] = {}
#     rst['historical']['dates'] = [season['s1'][0],
#                                   season['s1'][1],
#                                   season['s2'][0],
#                                   season['s2'][1],
#                                   season['s3'][0],
#                                   season['s3'][1],
#                                   season['s4'][0]]
#     rst['historical']['gdd'] = [int(round(gdd_s1)), int(round(gdd_s2)), int(round(gdd_s3))]
#     rst['historical']['avgtemp'] = [avglist(temp_s1), avglist(temp_s2), avglist(temp_s3)]
#
#     rst['predicted'] = {}
#     rst['predicted']['dates'] = milestone
#     rst['predicted']['gdd'] = predictedGdd
#     rst['predicted']['avgtemp'] = [avglist(avgtemp_curr[1]), avglist(avgtemp_curr[2]), avglist(avgtemp_curr[3])]
#
#     return rst



def calculateGddHourly(hisTempFile, hisRange, predictFile, predictStart):

    #  load all csv files
    predictFileFullPath = os.path.dirname(os.path.realpath(__file__)) + predictFile

    predictData = []

    with open(predictFileFullPath) as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)
        # remove header
        data.pop(0)
        # current date format: 2016-01-12
        currentDate = predictFile.split('_')[0]
        # loop each predicted row in the file
        for d in data:
            date = d[0].split('UTC')[0]
            temp = [currentDate, d[1], d[2], d[3]]

            # not valid prediction
            if float(d[1]) < -900:
                continue

            predictData.append([d[0], d[3]])

    predictData.sort(key=lambda x: x[0])

    # print data of current year
    # print('\n'.join(','.join(r) for r in predictData))

    # load help file [historical temporal file]
    helpFileDir = os.path.dirname(os.path.realpath(__file__)) + hisTempFile
    print('helpFileDir:', helpFileDir)

    hisData = []
    with open(helpFileDir) as help_file:
        reader = csv.reader(help_file)
        hisData = list(reader)
        hisData = hisData[1:]

    # load season aggregation file
    # seasonFile = os.path.dirname(os.path.realpath(__file__)) + hisSeasonFile
    # print('seasonFile:', seasonFile)

    # season = {}
    # with open(seasonFile) as data_file:
    #     season = json.load(data_file)

    # print(season)

    # gdd_s1 = 0
    # gdd_s2 = 0
    # gdd_s3 = 0
    #
    # temp_s1 = []
    # temp_s2 = []
    # temp_s3 = []

    # calculate gdd

    hisGdd = 0
    hisTemp = []

    for val in hisData:
        date = val[0]
        temp = float(val[1])

        if hisRange[0] <= date <= hisRange[1]:
            hisGdd += getGdd(temp)
            hisTemp.append(temp)
            print(date, temp, getGdd(temp), hisGdd)

    # print('gdd_s1', gdd_s1, 'gdd_s2', gdd_s2, 'gdd_s3', gdd_s3)

    # predict new season

    # specify start date
    # startDate = '2016-03-01'

    startDate = predictStart

    # currSeason = 1
    # gdd = [0, gdd_s1, gdd_s2, gdd_s3]
    # avgtemp_curr = [0,[],[],[]]
    # sum = 0
    # milestone = [startDate]
    # predictedGdd = []

    predictGdd = 0
    predictTemp = []

    predictEnd = 0
    for idx, data in enumerate(predictData):

        if data[0] < startDate:
            continue

        temp = float(data[1])
        predictGdd += getGdd(temp)
        predictTemp.append(temp)
        print(data[0], temp, getGdd(temp), predictGdd)

        if predictGdd >= hisGdd:
            predictEnd = data[0]
            break

    rst = {}
    rst['historical'] = {}
    rst['historical']['dates'] = hisRange
    rst['historical']['gdd'] = hisGdd
    rst['historical']['avgtemp'] = avglist(hisTemp)

    rst['predicted'] = {}
    rst['predicted']['dates'] = [predictStart, predictEnd]
    rst['predicted']['gdd'] = predictGdd
    rst['predicted']['avgtemp'] = avglist(predictTemp)

    return rst


if __name__ == '__main__':

    # hisTempFile = '//dat//tempDat//biale_weather_2014.csv'
    # hisSeasonFile = '//dat//seasonDat//season_test.json'
    # predictTempFolder = '//csv'
    # predictBudBreakDate = '2016-05-10'
    #
    # rst = calculateGdd(hisTempFile, hisSeasonFile, predictTempFolder, predictBudBreakDate)

    ################# parameter specification #####################

    hisYear = '2014'
    preYear = '2016'

    hisStart = '05-19'
    hisEnd = '09-15'

    preStart = '05-10'
    ################################################################

    hisTempFile = '//dat//tempDat//biale_weather_' + hisYear + '.csv'
    predictTempFolder = '//csv'

    rst = calculateGdd(hisTempFile, [hisYear+'-'+hisStart, hisYear+'-'+hisEnd], predictTempFolder, preYear+'-'+preStart)
    print(rst['historical']['dates'])
    print(rst['predicted']['dates'])
    print(rst)
