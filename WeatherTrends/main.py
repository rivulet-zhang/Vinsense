import os
import json

if __name__ == '__main__':

    #  load all json files
    jsonDir = os.path.dirname(os.path.realpath(__file__)) + '\data\json'
    print(jsonDir)

    json_files = [pos_json for pos_json in os.listdir(jsonDir) if pos_json.endswith('.json')]
    print('number of files:', len(json_files))

    for js in json_files:
        with open(os.path.join(jsonDir, js)) as json_file:
            # print(json.load(json_file))
            print()
