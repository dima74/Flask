# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, request, abort, session, redirect, url_for, g
from hashlib import md5
from functools import wraps

from flask import make_response
import pymysql

app = Flask("Simple app")
template_dir = 'templates'

APP_ID = '5737145'
SECRET_KEY = '2834bLZVu3IIfPtDkwI5'


@app.route('/chat')
def chat_render():
    messages = [("msg1", [("t1", "n1", "http://ya.ru")] * 2), ("msg2", [("t2", "n2", "http://google.com")] * 3)]
    return render_template("chat.html", messages=messages)


@app.route('/css/<path:path>')
def send_js(path):
    return send_from_directory('css', path)


@app.route('/iter_data_base')
def fetchdb():
    db = pymysql.connect("localhost", "amarokuser", "7966915", "amarokdb")
    cursor = db.cursor()
    sql = "SELECT * FROM genres"
    try:
        cursor.execute(sql)
        rv = cursor.fetchall()
        return render_template('iterdb.html', rv=rv)
    except:
        abort(501)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'vkid' in session:
            session['next'] = request.url
            return redirect(url_for('auth'))
        
        if session.get('vkhash', None) != md5((APP_ID + session['vkid'] + SECRET_KEY).encode('utf-8')).hexdigest():
            session.clear()
            session['next'] = request.url
            return redirect(url_for('auth'))
        
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def main():
    chats = [("n1", "http://google.com"), ("n2", "http://yandex.com")]
    return render_template('index.html', vkhash=session.get('vkid', None), chats=chats)


@app.route('/secret')
@login_required
def secret():
    return "Secret!"
    pass


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/auth-success')
def auth_success():
    session['vkid'] = request.args.get('uid')
    session['vkhash'] = request.args.get('hash')
    return redirect(session.get('next', "/"))


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0')
