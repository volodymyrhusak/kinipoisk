# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from select_insert_db import insert_data


def get_id_film(html):
    soup = BeautifulSoup(html)
    div = soup.find('div', class_='element most_wanted')
    p = div.find('p', class_='name')
    id_film = p.a['href']
    print id_film
    return id_film


def get_studio(urlListStudio):
    urlStudioFilmDict = {}
    soupStudio = BeautifulSoup(htmlListStudio)
    divListStudio = soupStudio.find(
        'div', style="margin-left: 64px; text-align: left")
    studioTable = divListStudio.find_all('table')[0]
    studio = studioTable.find_all('td')
    for td in studio:
        if td.a:
            urlStudioFilmDict[td.a.text.encode(
                'utf-8')] = 'http://www.kinopoisk.ru/' + td.a['href']

    print urlStudioFilmDict
    return ','.join(urlStudioFilmDict.keys())


def parse_film(html):
    year = u'год'
    slogan = u'слоган'


# Ceate soup
    soupFilm = BeautifulSoup(html)


# get film name
    divName = soupFilm.find('div', id='headerFilm')
    filmNameRus = divName.h1.text.encode('UTF-8')

# get film descr
    film_descr = soupFilm.find(
        'div', class_="block_left_padtop").find(
        'div', class_="brand_words").text.encode('UTF-8')

# get film year and slogan
    infoDiv = soupFilm.find("div", id="infoTable")
    infoTable = infoDiv.find_all('tr')

    for tr in infoTable:
        a = tr.td.text
        if a == year:
            print 'a ==year'
            film_year = tr.div.a.text
        elif a == slogan:
            print 'a ==slogan'
            film_slogan = tr.find_all('td')[1].text.encode('UTF-8')


# get review
    film_res = soupFilm.find_all("div", class_="reviewItem userReview")
    review = str()
    for data in film_res:
        review = review + data.find('span',
                                    class_='_reachbanner_').text.encode('UTF-8')
    img_url = soupFilm.find('div', class_="film-img-box").img['src']
    img_requests = requests.get(img_url).content

    return filmNameRus, film_year, film_slogan, film_descr, img_requests, review


def get_data(htmlFilm, htmlListStudio):
    dataFilm = parse_film(htmlFilm)
    studio = get_studio(htmlListStudio)
    insert_data(dataFilm, studio)
