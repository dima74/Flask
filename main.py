# -*- coding: utf-8 -*-
from flask import Flask, render_template, send_from_directory, request, abort, session, redirect, url_for, g
from hashlib import md5
from functools import wraps
#md5.new('').digest()

app = Flask("Simple app")
template_dir = 'templates'

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if not 'vkid' in session:
			session['next'] = request.url
			return redirect(url_for('auth'))
		return f(*args, **kwargs)
	return decorated_function

@app.route('/')
def main():
	return render_template('index.html', vkhash=session.get('vkid', None))

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
	app.run(debug=True, host='0.0.0.0', port=80)
