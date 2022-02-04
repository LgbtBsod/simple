import time
from flask import Flask, request, abort, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email

app = Flask(__name__)

m = []

users = {}


@app.route("/")
def hello_view():
    return '<a href="/Status">status</a'


@app.route('/Status')
def status_view():
    return {
        'status': True,
        'time': time.time(),
        'name': 'project',
        'users': len(users),
        'message': len(m)
    }



@app.route("/send", methods=['POST'])
def send_view():

    nick = request.json.get('name')
    password = request.json.get('password')
    text = request.json.get('text')
    for token in [nick, password, text]:
        if not isinstance(token, str) or not token or len(token) > 1024:
            abort(400)

    if nick in users:
        if users[nick] != password:
            abort(401)
    else:
        users[nick] = password

    m.append({'name': nick, 'time': time.time(), 'text': text})
    return {'ok': True}


def filters_message(e, key, m_v):
    new_e = []
    for x in e:
        if x[key] > m_v:
            new_e.append(x)

    return new_e


@app.route('/messages')
def messages_view():
    try:
        after = float(request.args['after'])
    except:
        abort(400)
    f_m = filters_message(m, key='time', m_v=after)
    return {'messages': f_m}


app.run()
