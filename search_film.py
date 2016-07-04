# -*- coding: utf-8 -*-
from flask import Flask, render_template, request ,redirect
from flask.ext.images import resized_img_attrs
from get_page import make_url,select_film,select_studio_film
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/post_film', methods=["POST"])
def search_in_page():
	filmName=request.form['filmName']
	if not filmName:
		return render_template('home.html')

	
	idkinopoiskfilm=make_url(filmName)
	
	
	return redirect('/film/<%s>'%(idkinopoiskfilm))
	#return redirect( render_template('film.html'))

# @app.route('/film/<studio><year>')
# def search_in_db(studio,year):	
# 	pass

@app.route('/film/<idkinopoiskfilm>')
def film_list(idkinopoiskfilm):

	filmData=select_film(idkinopoiskfilm)

	return render_template ('film.html' ,filmData=filmData )



@app.route('/studio_film/<studio>')
def studio_film(studio):

	filmList=select_studio_film(studio) 
	return render_template ('studio_film.html', filmList=filmList)
 


@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()

if __name__ == '__main__':
	app.run(debug=True)