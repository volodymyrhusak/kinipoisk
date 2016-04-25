# -*- coding: utf-8 -*-
import MySQLdb
import base64

def db_connect():
    print "___________________________________________db_connect___________________________________________"
    try:
        db=MySQLdb.connect(host='localhost', user='root',passwd='123',db='lodkotest')
        dbCursor=db.cursor()

    except MySQLdb.OperationalError:
        print 'Create db lodkotest'
        db=MySQLdb.connect(host='localhost', user='root',passwd='123')
        dbCursor=db.cursor()
        dbCursor.execute('CREATE DATABASE lodkotest DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci')

    dbCursor.execute('COMMIT')
    
    dbCursor.execute("SET NAMES utf8 COLLATE utf8_unicode_ci ;") #or utf8 or any other charset you want to handle
    dbCursor.execute("SET CHARACTER SET utf8;") #same as above


    
    try:
        dbCursor.execute('SELECT 1 FROM kinopoiskfilm')
    except MySQLdb.ProgrammingError:
        print  'CREATE TABLE kinopoiskfilm'
        dbCursor.execute('''CREATE TABLE kinopoiskfilm (
            idkinopoiskfilm INT PRIMARY KEY AUTO_INCREMENT, 
            name VARCHAR(20), 
            slogan VARCHAR(100),
            descr VARCHAR(1000),
            year VARCHAR(15),
            studio VARCHAR(1000)
            )DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci
            ''')

     
    try:
        dbCursor.execute('SELECT 1 FROM filmimage')
    except MySQLdb.ProgrammingError:
        print  'CREATE TABLE filmimage'
        dbCursor.execute('CREATE TABLE filmimage (idfilmimage INT PRIMARY KEY AUTO_INCREMENT, imagefilm LONGBLOB, idkinopoiskfilm INT,reviewdescr LONGTEXT)DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci')

    # try:
    #     dbCursor.execute('SELECT 1 FROM review')
    # except MySQLdb.ProgrammingError:
    #     print  'CREATE TABLE review'
    #     dbCursor.execute('CREATE TABLE review (idreview INT PRIMARY KEY AUTO_INCREMENT, idkinopoiskfilm INT,reviewdescr LONGTEXT)DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci')
    dbCursor.execute('COMMIT')
    return db

def insert_data(data,studio):
	db=db_connect()
	print "___________________________________________insert_data___________________________________________"
	filmNameRus=data[0]
	film_year=data[1]
	film_slogan=data[2]
	film_descr=data[3]
	img_requests=base64.b64encode(data[4])
	film_res=data[5]
	dbCursor=db.cursor()

	dbCursor.execute('SELECT idkinopoiskfilm FROM kinopoiskfilm where name = "%s" '%filmNameRus)
	idkinopoiskfilm=dbCursor.fetchone()[0]
	if not idkinopoiskfilm:
		dbCursor.execute('INSERT INTO kinopoiskfilm (name,slogan,descr,year,studio)VALUE("%s","%s","%s","%s","%s")'%(filmNameRus,film_slogan,film_descr,str(film_year),studio))
		dbCursor.execute('COMMIT')

		dbCursor.execute('SELECT max(idkinopoiskfilm) FROM kinopoiskfilm WHERE name="%s"'%(filmNameRus))
		idkinopoiskfilm=dbCursor.fetchone()[0]
		    
		dbCursor.execute('INSERT INTO filmimage (imagefilm,idkinopoiskfilm,reviewdescr)VALUE("%s",%s,"%s")'%(img_requests,idkinopoiskfilm,film_res))
		dbCursor.execute('COMMIT')
	


	
	
	return idkinopoiskfilm

def select_data(idkinopoiskfilm):
	db=db_connect()
	dbCursor=db.cursor()
	print idkinopoiskfilm
	dbCursor.execute('''select k.name, k.slogan, k.descr,k.year,k.studio, f.reviewdescr, f.imagefilm  
                        from kinopoiskfilm k 
                        join filmimage f on f.idkinopoiskfilm=k.idkinopoiskfilm 
                        where k.idkinopoiskfilm=1''')
	dataFilm=dbCursor.fetchone()
	response ={
	'filmName':dataFilm[0].decode('utf-8'),
	'filmSlogan':dataFilm[1].decode('utf-8'),
	'filmDescr':dataFilm[2].decode('utf-8'),
	'filmYear':dataFilm[3].decode('utf-8'),
	'filmStudio':dataFilm[4].decode('utf-8').split(','),  #.split(',')
	'filmReviedescr':dataFilm[5].decode('utf-8'),
	'filmImage':base64.b64decode(dataFilm[6])
	}
	#print response 
	#print response['filmStudio']
	return response

def select_studio_data(studio):
    db=db_connect()
    dbCursor=db.cursor()
    dbCursor.execute('''select k.name, k.descr ,k.idkinopoiskfilm 
                        from kinopoiskfilm k 
                        where k.studio like "%'''+studio+'''%" ''')
    data=dbCursor.fetchall()
    response=[]
    for film in data:
    	# film[0].decode('utf-8')
    	# film[1].decode('utf-8')
    	response.append((film[0].decode('utf-8'),film[1].decode('utf-8'),film[2]))
    #print  response 
    return response