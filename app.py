import random
import datetime
from flask import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def getLastDate():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

cnt = -1
bless = {}

def getmessages():
    try:
        f = open('bless.txt', 'r')
        while True:
            global cnt
            time = f.readline()
            if time:
                cnt = cnt + 1
                name = f.readline()
                message = f.readline()
                mes = []
                mes.append(time)
                mes.append(name)
                mes.append(message)
                bless[cnt] = mes
            else:
                break
    finally:
        if f:
            f.close()

def add_message(time, name, message):
    try:
        f = open('bless.txt', 'a')
        f.write(time + '\n')
        f.write(name + '\n')
        f.write(message + '\n')
    finally:
        if f:
            f.close()

app = Flask(__name__)

app.secret_key = "2001013020010905"

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/poor')
def poor():
    return render_template('poor.html')

@app.route('/real_lucky', methods = ['GET', 'POST'])
def real_lucky():
    if request.method == 'GET':
        return render_template('real_lucky.html', data = bless)
    else:
        global cnt
        cnt = cnt + 1
        name = request.form['name']
        message = request.form['message']
        time = getLastDate()
        add_message(time, name, message)
        mes = []
        mes.append(time)
        mes.append(name)
        mes.append(message)
        bless[cnt] = mes
        return redirect('/real_lucky')

@app.route('/i_love_you', methods = ['GET', 'POST'])
def i_love_you():
    if request.method == 'GET':
        return render_template('lucky.html')
    else:
        lucky = request.form['lucky']
        if lucky == "2020luckydog":
            return redirect('/real_lucky')
        else:
            return redirect('/')

@app.route('/password', methods = ['GET', 'POST'])
def password():
    if request.method == 'GET':
        return render_template('password.html'), 20010905
    else:
        serect = request.form['serect']
        if serect == "20010905": return redirect('/i_love_you')
        else: return redirect('/poor')
    

if __name__ == '__main__':
    getmessages()
    app.run(host = '0.0.0.0', port = '2020', debug = True)
