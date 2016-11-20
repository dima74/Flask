# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, request, abort, session, redirect, url_for, make_response
from hashlib import md5
from functools import wraps
import pymysql
import urllib

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

app = Flask("Simple app", static_folder="/var/www/html")
template_dir = 'templates'


# @app.route('/home/ulyanin/')
# def send_fonts(path):
#     return send_from_directory('fonts', path)


def getDataBase():
    return pymysql.connect(SERVER_ADDRESS, MYSQL_USER, MYSQL_PASS, MYSQL_DB, charset="utf8")


@app.route('/chat/search', methods=['GET', 'POST'])
def search():
    print("render_search")
    if request.method == "GET":
        print("get")
        db = getDataBase()
        print("1")
        c = db.cursor()
        print("2")
        print(request.form)
        print('''select * from Messages where userId = %s''' % request.args['search'])
        c.execute('''select * from Messages where userId = %s''' % request.args['search'])
        print("3")
        records = c.fetchall()
        print("rec = ", records)
        return render_template("results.html", records=records)
    return render_template('chat.html')


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('fonts', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)


@app.route('/files/<path:path>')
def send_files(path):
    return send_from_directory('files', path)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not 'vkid' in session:
            session['next'] = request.url
            return redirect(url_for('main'))

        # if session.get('vkhash', None) != md5((APP_ID + session['vkid'] + SECRET_KEY).encode('utf-8')).hexdigest():
        #     session.clear()
        #     session['next'] = request.url
        #     return redirect('/intro')
        if 'vkhashpart' not in session or session.get('vkhash', None) != md5((session['vkhashpart'] + SECRET_KEY).encode('utf-8')).hexdigest():
            session.clear()
            session['next'] = request.url
            return redirect(url_for('main'))
        return f(*args, **kwargs)

    return decorated_function


def runSql(sql):
    print(10)
    db = getDataBase()
    print(11)
    cursor = db.cursor()
    print(12)
    try:
        cursor.execute(sql)
        print(13)
        rv = cursor.fetchall()
        return rv
    except:
        abort(501)


@app.route('/')
def main():
    if not 'vkid' in session:
        return render_template('intro.html')
    else:
        chats = runSql("SELECT ChatNames.chatId, ChatNames.name FROM ChatsToUsers, ChatNames WHERE ChatNames.chatId = ChatsToUsers.chatId and ChatsToUsers.userId = %s" % session['vkid'])
        chats = [{"name": chat[1], "url": url_for('chatPage', chatId=chat[0])} for chat in chats]
        return render_template('intro.html', chats=chats)


@app.route('/chat')
@login_required
def chatPage():
    chatId = request.args.get('chatId', None)
    # if chatId is None:
    #     return redirect("/")

    # search_sring = request.args.get('search', "")
    # search_sring = request.args.get('search', "").decode("utf-8")
    # search_sring = urllib.unquote(unicode(request.args.get('search', "")))
    search_string = request.args.get('search', "")
    # print("search_sring = ", search_string)
    search_string = search_string.encode("utf-8")
    print("search_sring = ", search_string)

    messageContentFilter = "AND INSTR(Messages.content, '%s') > 0" % search_string if search_string else ""
    print(0)
    chatFilter = "AND Messages.chatId = '%s'" % chatId if chatId else "AND Messages.chatId IN (SELECT chatId FROM ChatsToUsers WHERE userId = '%s')" % session['vkid']
    print(1)
    chatName = runSql("SELECT name FROM ChatNames WHERE chatId = '%s'" % chatId)[0][0] if chatId else None
    print(2)
    print("chatId = ", chatId)
    print("messageContentFilter = ", messageContentFilter)
    print("chatFilter = ", chatFilter)
    sql = """SELECT Messages.messageId, Messages.content, UserNames.name
             FROM Messages, UserNames
             WHERE Messages.userId = UserNames.userId %s %s""" % (chatFilter, messageContentFilter)
    print(sql)
    messages = runSql(sql)
    # print(messages)
    # print()
    # print()
    tuple_append = lambda tup, elem: tuple(list(tup) + [elem])
    print(3)
    messages_new = []
    print(4)
    for message in messages:
        print(5)
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
            d = dict(zip(("type", "path", "name"), messageFile))
            if d["type"] != 5 and d["type"] != 2:
                d["path"] = d["path"][13:]
            attachments[messageFile[0] - 1].append(d)
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
    print('end')
    print(message)
    print(chatName)
    return render_template('results.html', messages=messages_new, chatName=chatName)


@app.route('/intro')
def intro():
    return render_template('intro.html')


# @app.route('/auth-success')
# def auth_success():
#     session['vkid'] = request.args.get('uid')
#     session['vkhash'] = request.args.get('hash')
#     return redirect(session.get('next', "/"))


@app.route('/oauth-success')
def oauth_success():
    session['vkid'] = request.args.get('uid')
    session['vkfirst'] = request.args.get('first')
    session['vklast'] = request.args.get('last')
    session['vkid'] = request.args.get('uid')
    session['vkhash'] = request.args.get('sig')
    session['vkhashpart'] = request.args.get('hashpart')
    return redirect(session.get('next', "/"))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/oauth')
def auth():
    return render_template('oauth.html')


@app.route('/template')
def template():
    return render_template('template.html')


@app.route('/print_cookie')
def print_cookie():
    print(session)
    print(request.cookies)
    return 'test'


if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True, host='0.0.0.0', threaded=True, port=80)
