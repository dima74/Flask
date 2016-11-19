# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_from_directory, request, abort, session, redirect

app = Flask("Simple app")

template_dir = 'templates'

@app.route('/test')
def users():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
