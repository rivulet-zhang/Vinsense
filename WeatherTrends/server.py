from bottle import route, run, template
import calcgdd
import json
import sys

@route('/getgdd', method="GET")
def index():
    rst = calcgdd.calculateGdd()
    return json.dumps(rst)

ip = sys.argv[1]
port = int(sys.argv[2])

run(host=ip, port=port)