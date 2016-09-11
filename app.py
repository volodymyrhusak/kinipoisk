# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, session, url_for
from get_page import make_url, select_film, select_studio_film
from select_insert_db import select_user, select_data
from functools import wraps
app = Flask(__name__)

app.secret_key='secret'


def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'username' in session:
			return f(*args, **kwargs)
		else:
			return redirect(url_for('login'))
	return wrap


@app.route('/')
@login_required
def home():
	userName=session['username']
	films=select_data(userName=userName)
	userData={'user':userName,
	'films':films}
    return render_template('home.html' , userData=userData)

@app.route('/login', methods=["GET","POST"])
def login():
	if request.method=="GET":
		return render_template('login.html')
	elif request.method=="POST":
		userName = request.form['userName']
		password = request.form['password']
		if select_user(userName,password):
			session['username'] = userName
			return redirect(url_for('home'))
		else:
			return redirect(url_for('login'))


@app.route('/post_film', methods=["POST"])
@login_required
def search_in_page():
    filmName = request.form['filmName']
    if not filmName:
        return render_template('home.html')
    idkinopoiskfilm = make_url(filmName)
    return redirect('/film/<%s>' % (idkinopoiskfilm))


@app.route('/film/<idkinopoiskfilm>')
@login_required
def film_list(idkinopoiskfilm):

    filmData = select_film(idkinopoiskfilm)

    return render_template('film.html', filmData=filmData)


@app.route('/studio_film/<studio>')
@login_required
def studio_film(studio):

    filmList = select_studio_film(studio)
    return render_template('studio_film.html', filmList=filmList)


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
