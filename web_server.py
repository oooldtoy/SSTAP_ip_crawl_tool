from flask import *
import sqlite3,time

app = Flask(__name__)

def timenow(timepoint):#转换时间戳
    timeArray = time.localtime(timepoint)
    timetranslate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return timetranslate

@app.route('/')
def main():
    con = sqlite3.connect('rules_data.db')
    cu = con.cursor()
    data = cu.execute("select rules,ip,time from rules")
    data_list = []
    for rules,ip,time in data:
        rules = rules.replace('\n','<br/>')
        time = timenow(time)
        data_list.append([rules,ip,time])
    cu.close()
    con.close()
    data_list = list(reversed(data_list))#反转列表，最新的在最前面
    return render_template('main.html',data=data_list)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5001)
