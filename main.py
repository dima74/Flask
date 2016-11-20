# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, request, abort, session, redirect, url_for, make_response
from hashlib import md5
from functools import wraps
import pymysql

APP_ID = '5737145'
SECRET_KEY = '2834bLZVu3IIfPtDkwI5'
MYSQL_USER = "kipomur"
MYSQL_PASS = "praiseMUR"
MYSQL_DB = "miptvkbot"
SERVER_ADDRESS = "10.55.166.244"
# SERVER_ADDRESS = "localhost"
# MYSQL_USER = "root"
# MYSQL_PASS = "7966915"
# MYSQL_DB = "test"

app = Flask("Simple app")
template_dir = 'templates'


@app.route('/css/<path:path>')
def send_js(path):
    return send_from_directory('css', path)


@app.route('/iter_data_base')
def fetchdb():
    db = pymysql.connect(SERVER_ADDRESS, "amarokuser", "7966915", "amarokdb", charset="utf8")
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
    db = pymysql.connect(SERVER_ADDRESS, MYSQL_USER, MYSQL_PASS, MYSQL_DB, charset="utf8")
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
    db = pymysql.connect(SERVER_ADDRESS, MYSQL_USER, MYSQL_PASS, MYSQL_DB, charset="utf8")
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
    chatName = runSql("SELECT name FROM ChatNames WHERE chatId = %s" % (chatId))
    sql = """SELECT Messages.messageId, Messages.content, UserNames.name
             FROM Messages, UserNames
             WHERE Messages.userId = UserNames.userId AND Messages.chatId = %s""" % (chatId)
    messages = runSql(sql)
    # print(chatId)
    # print(messages)
    # print()
    # print()
    tuple_append = lambda tup, elem: tuple(list(tup) + [elem])
    messages_new = []
    for message in messages:
        # print(message)
        sql2 = "SELECT type, path, name FROM FileLinks WHERE messageId = %d" % (message[0])
        files = runSql(sql2)
        if not files:
            continue
        # print(files)
        # nameType = dict(zip(range(1, 6), ["photo", "video", "audio", "doc", "link"]))
        # attachments = dict(zip(["photo", "video", "audio", "doc", "link"], [[] for i in range(6)]))
        # nameType = dict(zip(range(1, 6), ["photo", "video", "audio", "doc", "link"]))
        attachments = [[] for _ in range(5)]
        for messageFile in files:
            attachments[messageFile[0] - 1].append(dict(zip(("type", "path", "name"), messageFile)))
        # print()
        # print('attachments = ', attachments)
        # print('dict = ', dict(zip(("photo", "video", "audio", "doc", "link"), attachments)))
        # print()
        messages_new.append(dict(zip(("messageId", "messageContent", "userName", "files"),
                                     tuple_append(message, dict(zip(("photo", "video", "audio", "doc", "link"), attachments))))))
        # print('concat = ', tuple_append(message, dict(zip(("photo", "video", "audio", "doc", "link"), attachments))))
        # print('dict = ', dict(zip(("messageId", "messageContent", "userName", "files"),
        #                           tuple_append(message, dict(zip(("photo", "video", "audio", "doc", "link"), attachments))))))
    # print()
    # for message in messages_new:
    #     print(message)
    # print('before')
    # print(messages_new[0]['messageId'])
    # print('after')
    return render_template('chat.html', messages=messages_new, chatName=chatName)


@app.route('/intro')
def intro():
    return render_template('intro.html')


@app.route('/auth-success')
def auth_success():
    session['vkid'] = request.args.get('uid')
    session['vkhash'] = request.args.get('hash')
    return redirect(session.get('next', "/"))


@app.route('/auth')
def auth():
    return render_template('oauth.html')


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0')
