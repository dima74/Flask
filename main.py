# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_from_directory, request, abort, session, redirect

from flask import make_response
import pymysql

app = Flask("Simple app")
template_dir = 'templates'

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



@app.route('/')
def users():
    return render_template('index.html', session=session)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

