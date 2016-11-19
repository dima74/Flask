# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_from_directory, request, abort, session, redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app, MYSQL_USER='kipomur', MYSQL_PASSWORD='praiseMUR')

@app.route('/')
def users():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT user, host FROM mysql.user''')
    rv = cur.fetchall()
    return str(rv)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
