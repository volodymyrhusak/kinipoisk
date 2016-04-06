# -*- coding: utf-8 -*-
from flask import Flask, render_template, request ,redirect
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/film', methods=["POST"])
def search_in_page():
	filmName=request.form['filmName']
	return redirect('/film_good')

# @app.route('/film/<studio><year>')
# def search_in_db(studio,year):	
# 	pass

@app.route('/film_good')
def film_list():
	return '<p>GOOD!!</p>'

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()

if __name__ == '__main__':
	app.run(debug=True)