import flask
from flask import Flask, abort
import time
from datetime import datetime
import random

app = Flask(__name__)
db = []
for i in range(3):
    db.append({
        'name': 'Anton',
        'time': 12343,
        'text': 'text01923097'
    })

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/send", methods= ['POST'])
def send_message():
    '''
    функция для отправки нового сообщения пользователем
    :return:
    '''

    data = flask.request.json
    if not isinstance(data, dict):
        return abort(400)

    if 'name' not in data or \
        'text' not in data:
        return abort(400)

    if not isinstance(data['name'], str) or \
        not isinstance(data['text'], str) or \
        len(data['name']) == 0 or \
        len(data['text']) == 0:
        return abort(400)

    text = data['text']
    name = data['name']
    message = {
        'text': text,
        'name': name,
        'time': time.time()
    }
    if text[:4] == 'anon': #если сообщение начинается со слова anon, то оно должно быть анонимным
        message['name'] = 'Аноним'
        message['text'] = text[4:]
    db.append(message)
    
    if text == '/help':
        answer = {
            'text': '/help -- вывести список команд\n/emoji -- эмоция во время программирования\n/coin -- подбросить монетку\n/random -- введите числа через пробел',
            'name': 'Бот',
            'time': time.time()
        }
    elif text == '/emoji':
        answer = {
            'text': ' ¯\_(ツ)_/¯ ',
            'name': 'Бот',
            'time': time.time()
        }
    elif text[:7] == '/random':
        start, end = text[7:].split()
        rez = random.randint(int(start), int(end))
        answer = {
            'text': str(rez),
            'name': 'Бот',
            'time': time.time()
        }
    elif text == '/coin':
        if random.randint(0,1):
            answer = {
                'text': 'Орёл',
                'name': 'Бот',
                'time': time.time()
            }
        else:
            answer = {
                'text': 'Решка',
                'name': 'Бот',
                'time': time.time()
            }
    db.append(answer)
    return {'ok': True}

def anonym():...

@app.route("/messages")
def get_messages():
    try:
        after = float(flask.request.args['after'])
    except:
        abort(400)
    db_after = []
    for message in db:
        if message['time'] > after:
            db_after.append(message)
    return {'messages': db_after}

@app.route("/status")
def print_status():
    output = 'OK!<br>'
    t = time.time()
    dt = datetime.fromtimestamp(t)
    output += dt.strftime('%Y-%m-%d %H:%M:%S') + '<br>'
    names = []
    for message in db:
        if message['name'] not in names:
            names.append(message['name'])
    N = len(names)
    output += 'Число пользователей:\t' + str(N) + '<br>' + 'Список пользователей:<br>'
    for i in names:
        output += i + '<br>'
    output += 'Число сообщений:\t' + str(len(db))
    return output

app.run()