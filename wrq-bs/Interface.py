from flask import Flask, request
from flask_cors import CORS
import sql
import json
import numpy as np
import time
import Excel

class avr_dict():
    def __init__(self, x, y):
        self.x = x
        self.y = y

def str2stamp(dt):
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S") #转换成时间数组
    timestamp = time.mktime(timeArray) #转换成时间戳
    return timestamp

def stamp2str(stamp, format):
    time_local = time.localtime(stamp) #转换成localtime
    dt = time.strftime(format, time_local) #转换成新的时间格式
    return dt

app = Flask(__name__)
CORS(app)
#获取数据
@app.route('/get_data', methods=['POST'])
def get_data():
    time = request.form.get("time")
    if time == '':
        return json.dumps(sql.mysql().search_last_hour())
    else:
        return json.dumps(sql.mysql().search_by_hour(time))

#获取平均数据
@app.route('/get_avr', methods=['POST'])
def get_avr():
    time = request.form.get("time")
    sensor = request.form.get("sensor")
    avr_list = []
    time_list = []
    for i in reversed(range(1,13)):
        hour_data_list = []
        hour_dict_list = sql.mysql().search_by_hour(stamp2str(str2stamp(time)-3600*i, "%Y-%m-%d %H:%M:%S"))
        time_list.append(stamp2str(str2stamp(time)-3600*i, "%H:%M"))
        for item in hour_dict_list:
            hour_data_list.append(float(item.get(sensor)))
        if len(hour_data_list) == 0:
            avr_list.append(0)
        else:
            avr_list.append(np.mean(hour_data_list))
    return json.dumps(avr_dict(time_list, avr_list).__dict__)

@app.route('/send_email', methods=['GET'])
def send_email():
    return str(Excel.mail(Excel.mem2xls(sql.mysql().search_last_hour())).send())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=39121, threaded=True, debug=True)