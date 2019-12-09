from flask import *
from datetime import timedelta
import sqlite3,time,os
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
data_base = config.data_base


@app.route('/')
def hello_world():
    return 'hello world'


user_list = [[config.password,config.username]]

def timenow(timepoint):#转换时间戳
    timeArray = time.localtime(timepoint)
    timetranslate = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return timetranslate

@app.route('/rules/')
def rules():
    con = sqlite3.connect(data_base)
    cu = con.cursor()
    data = cu.execute("select rules,process,ip,time from rules")
    data_list = []
    for rules,process,ip,time in data:
        rules = rules.replace('\n','<br/>')
        ip = ip.split('.')
        ip[2] = '*'
        ip[3] = '*'
        ip = '.'.join(ip)
        time = timenow(time)
        data_list.append([rules,process,ip,time])
    cu.close()
    con.close()
    data_list = list(reversed(data_list))#反转列表，最新的在最前面
    return render_template('rules.html',data=data_list)

@app.route('/rules/login/',methods=['POST','GET'])
def rules_login():
    if session.get('username'):
        return redirect(url_for('rules_modify'))
    else:
        if request.method=='GET':
            return render_template('rules_login.html')
        else:
            username = request.form.get('username')
            password = request.form.get('password')
            print(username,password)
            if [password,username] in user_list:
                session['username'] = username#登陆成功设置session
                session.permanent = True#
                app.permanent_session_lifetime = timedelta(minutes=10)#设置session到期时间
                return redirect(url_for('rules_modify'))
            else:
                return render_template('rules_login.html')

@app.route('/rules/modify/',methods=['POST','GET'])
def rules_modify():
    if session.get('username'):
        con = sqlite3.connect(data_base)
        cu = con.cursor()
        data = cu.execute("select rules,process,ip,time,version from rules")
        data_list = []
        for rules,process,ip,time,version in data:
            rules = rules.replace('\n','<br/>')
            data_list.append([rules,process,ip,time,version])
        cu.close()
        con.close()
        if request.method=='GET':
            data_list = list(reversed(data_list))#反转列表，最新的在最前面
            return render_template('rules_modify.html',data=data_list)
        else:
            #print(data_list)
            data_post = str(request.form)  # 如果是get请求就用args
            data_post = data_post.replace('ImmutableMultiDict', '')
            data_post = tuple(eval(data_post))
            data_temp = []
            for i in data_post:
                data_temp.append(i[0])
            print(data_temp)
            for i in data_temp:
                con = sqlite3.connect(data_base)
                cu = con.cursor()
                data = cu.execute("delete from rules where time = {}".format(i))
                con.commit()
                data = cu.execute("select rules,process,ip,time,version from rules")
                data_list = []
                for rules,process,ip,time,version in data:
                    rules = rules.replace('\n','<br/>')
                    data_list.append([rules,process,ip,time,version])
                cu.close()
                con.close()
            data_list = list(reversed(data_list))#反转列表，最新的在最前面
            return render_template('rules_modify.html',data=data_list)
    else:
        return redirect(url_for('rules_login'))

if __name__=='__main__':
    app.run(host='0.0.0.0',port=config.web_port)


