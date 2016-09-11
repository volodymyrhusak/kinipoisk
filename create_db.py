# -*- coding: utf-8 -*-
from config import DB
import MySQLdb
def main():

    print 'Create db lodkotest'
    db = MySQLdb.connect( host=DB['host'],
        user=DB['user'],
        passwd=DB['passwd'])
    dbCursor = db.cursor()
    dbCursor.execute('''CREATE DATABASE lodkotest 
            DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci''')
    dbCursor.execute('COMMIT')
    print 'Successful create db lodkotest'
    db.close()
    

    db = MySQLdb.connect(
        host=DB['host'],
        user=DB['user'],
        passwd=DB['passwd'],
        db=DB['db'])
    
    dbCursor=db.cursor()
        # or utf8 or any other charset you want to handle
    dbCursor.execute("SET NAMES utf8 COLLATE utf8_unicode_ci ;")
    dbCursor.execute("SET CHARACTER SET utf8;")
    
    print 'CREATE TABLE kinopoiskfilm'
    dbCursor.execute('''CREATE TABLE kinopoiskfilm (
        idkinopoiskfilm INT PRIMARY KEY AUTO_INCREMENT,
        iduser INT NOT NULL,
        name VARCHAR(20),
        slogan VARCHAR(100),
        descr VARCHAR(1000),
        year VARCHAR(15),
        studio VARCHAR(1000),
        INDEX user_ind (iduser)
        )DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci''')
    print 'Successful create table kinopoiskfilm'
    
    print 'CREATE TABLE filmimage'
    dbCursor.execute('''CREATE TABLE filmimage (
        idfilmimage INT PRIMARY KEY AUTO_INCREMENT,
        imagefilm LONGBLOB,
        idkinopoiskfilm INT NOT NULL,
        reviewdescr LONGTEXT,
        INDEX kinop_ind (idkinopoiskfilm))
        DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci''')
    print 'Successful create table filmimage'

    print 'CREATE TABLE user'
    dbCursor.execute('''CREATE TABLE user (
        iduser INT PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL
        )DEFAULT CHARSET=utf8 DEFAULT COLLATE utf8_unicode_ci''')
    print 'Successful create table user'

    dbCursor.execute('''ALTER TABLE kinopoiskfilm 
        ADD FOREIGN KEY (iduser)
        REFERENCES user(iduser)
        ON DELETE CASCADE''')

    dbCursor.execute('''ALTER TABLE filmimage 
        ADD FOREIGN KEY (idkinopoiskfilm)
        REFERENCES kinopoiskfilm(idkinopoiskfilm)
        ON DELETE CASCADE''')

    dbCursor.execute('COMMIT')
    db.close()

if __name__ == '__main__':
    main()