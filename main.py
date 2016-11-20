# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, request, abort, session, redirect, url_for, g
from hashlib import md5
from functools import wraps

from flask import make_response
import pymysql

APP_ID = '5737145'
SECRET_KEY = '2834bLZVu3IIfPtDkwI5'
# MYSQL_USER = "kipomur"
# MYSQL_PASS = "praiseMUR"
# MYSQL_DB = "miptvkbot"
MYSQL_USER = "root"
MYSQL_PASS = ""
MYSQL_DB = "test"

app = Flask("Simple app")
template_dir = 'templates'


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
            return redirect('/intro')

        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
@login_required
def main():
    db = pymysql.connect("localhost", MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    sql = "SELECT chatId FROM ChatsToUsers WHERE userId = " + session['vkid']
    try:
        cursor.execute(sql)
        chatIds = cursor.fetchall()
        return render_template('index.html', rv=chatIds)
    except:
        abort(501)
        # return render_template('index.html', vkhash=session.get('vkid', None))


def runSql(sql):
    db = pymysql.connect("localhost", MYSQL_USER, MYSQL_PASS, MYSQL_DB)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        rv = cursor.fetchall()
        return rv
    except:
        abort(501)


@app.route('/chat')
# @login_required
def chatPage():
    chatId = request.args.get('chatId')
    sql = """SELECT Messages.messageId, Messages.content, UserNames.name, ChatNames.name
             FROM Messages, UserNames, ChatNames
             WHERE Messages.chatId = ChatNames.chatId AND Messages.userId = UserNames.userId AND Messages.chatId = %s""" % (chatId)
    messages = runSql(sql)
    concat = lambda tup, elem: tuple(list(tup) + [elem])
    messages_new = []
    for message in messages:
        sql2 = "SELECT type, path, name FROM FileLinks WHERE messageId = %d" % (message[0])
        files = runSql(sql2)
        files = [dict(zip(("type", "path", "name"), messageFile)) for messageFile in files]
        messages_new.append(dict(zip(("messageId", "messageContent", "userName", "chatName", "files"), concat(message, files))))
    # for message in messages_new:
    #     print(message)
    return render_template('test.html', messages=messages_new)


@app.route('/intro')
def auth():
    return render_template('intro.html')


@app.route('/auth-success')
def auth_success():
    session['vkid'] = request.args.get('uid')
    session['vkhash'] = request.args.get('hash')
    return redirect(session.get('next', "/"))


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0')
