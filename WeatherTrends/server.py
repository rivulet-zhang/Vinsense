from bottle import Bottle, request, response, run
import calcgdd
import json
import sys

app = Bottle()

@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS, GET'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.route('/getgdd', method="GET")
def index():

    try:
        hisYear = str(request.query.get("hisYear"))
        curYear = str(request.query.get("curYear"))
        vineyard = str(request.query.get("vineyard"))
        budbreak = str(request.query.get("budbreak"))

        if hisYear is None or curYear is None or vineyard is None or budbreak is None:
            raise

        print(hisYear, curYear, vineyard, budbreak)

        hisTempFile = '//biale//biale_weather_' + hisYear + '.csv'
        hisSeasonFile = '//biale//season_' + hisYear + '_bigranch.json'
        predictTempFolder = '//csv'
        predictBudBreakDate = budbreak

        rst = calcgdd.calculateGdd(hisTempFile, hisSeasonFile, predictTempFolder, predictBudBreakDate)
        return json.dumps(rst)
    except:

        print("error:", sys.exc_info())
        print("default setting:")
        # default settings:
        default_hisTempFile = '//biale//biale_weather_2014.csv'
        default_hisSeasonFile = '//biale//season_2014.json'
        default_predictTempFolder = '//csv'
        default_predictBudBreakDate = '2016-03-27'

        rst = calcgdd.calculateGdd(default_hisTempFile, default_hisSeasonFile, default_predictTempFolder, default_predictBudBreakDate)
        return json.dumps(rst)

ip = sys.argv[1]
port = int(sys.argv[2])

run(app, host=ip, port=port)