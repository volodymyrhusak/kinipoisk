# -*- coding: utf-8 -*-
import MySQLdb
import base64
from config import DB

def db_connect():
    db = MySQLdb.connect(
        host=DB['host'],
        user=DB['user'],
        passwd=DB['passwd'],
        db=DB['db'])
    dbCursor = db.cursor()

    # or utf8 or any other charset you want to handle
    dbCursor.execute("SET NAMES utf8 COLLATE utf8_unicode_ci ;")
    dbCursor.execute("SET CHARACTER SET utf8;")  # same as above
    return db


def insert_data(data, studio):
    db = db_connect()
    print "___________________________________________insert_data___________________________________________"
    filmNameRus = data[0]
    film_year = data[1]
    film_slogan = data[2]
    film_descr = data[3]
    img_requests = base64.b64encode(data[4])
    film_res = data[5]
    dbCursor = db.cursor()

    dbCursor.execute(
        'SELECT idkinopoiskfilm FROM kinopoiskfilm where name = "%s" and studio = "%s"' %
        (filmNameRus, studio))

    try:
        idkinopoiskfilm = dbCursor.fetchone()[0]
    except TypeError:
        dbCursor.execute(
            'INSERT INTO kinopoiskfilm (iduser,name,slogan,descr,year,studio)VALUE("%s","%s","%s","%s","%s")' %
            (filmNameRus, film_slogan, film_descr, str(film_year), studio))
        dbCursor.execute('COMMIT')

        dbCursor.execute(
            'SELECT LAST_INSERT_ID() FROM kinopoiskfilm')
        idkinopoiskfilm = dbCursor.fetchone()[0]

        dbCursor.execute(
            '''INSERT INTO filmimage (imagefilm,idkinopoiskfilm,reviewdescr)
            VALUE("%s",%s,"%s")''' %
            (repr(img_requests), idkinopoiskfilm, film_res))
        dbCursor.execute('COMMIT')

    return idkinopoiskfilm


def select_data(idkinopoiskfilm=None,userName):
    db = db_connect()
    dbCursor = db.cursor()
    response=[]
    print idkinopoiskfilm[1:-1]
    select = '''select k.name, k.slogan, k.descr,k.year,k.studio, f.reviewdescr, f.imagefilm
						from lodkotest.kinopoiskfilm k
                        join lodkotest.user u on u.iduser=k.iduser
                        join lodkotest.filmimage f on f.idkinopoiskfilm=k.idkinopoiskfilm
                        where (k.idkinopoiskfilm=%s and u.username=%s)
                        or u.username=%s''' % (idkinopoiskfilm[1:-1],userName,userName)
    print select
    dbCursor.execute(select)
    dataFilmList = dbCursor.fetchall()
    for dataFilm in dataFilmList:
        response.append({
                'filmName': dataFilm[0].decode('utf-8'),
                'filmSlogan': dataFilm[1].decode('utf-8'),
                'filmDescr': dataFilm[2].decode('utf-8'),
                'filmYear': dataFilm[3].decode('utf-8'),
                'filmStudio': dataFilm[4].decode('utf-8').split(','),  # .split(',')
                'filmReviedescr': dataFilm[5].decode('utf-8'),
                'filmImage': base64.b64decode(dataFilm[6])
            })
    # print response
    # print response['filmStudio']
    db.close()
    return response


def select_studio_data(studio):
    db = db_connect()
    dbCursor = db.cursor()
    dbCursor.execute('''select k.name, k.descr ,k.idkinopoiskfilm
                        from kinopoiskfilm k
                        where k.studio like "%''' + studio + '''%" ''')
    data = dbCursor.fetchall()
    response = []
    for film in data:
        # film[0].decode('utf-8')
        # film[1].decode('utf-8')
        response.append(
            (film[0].decode('utf-8'),
             film[1].decode('utf-8'),
                film[2]))
    # print  response
    db.close()
    return response

def select_user(login,passwd):
    db = db_connect()
    dbCursor = db.cursor()
    dbCursor.execute('''select 1
                        from user u
                        where u.username ="%s" and u.password="%s" '''%(str(login),str(passwd)))
    mark = dbCursor.fetchone()
    print mark
    db.close()
    if mark:
        return True
    else: 
        return False    
