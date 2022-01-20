from flask import Flask, render_template
from utils import *

app = Flask(__name__)


@app.route('/movie/<title>', )
def page_movie(title):
    movie = get_movie_by_id(title)
    return render_template('movie.html', movie=movie)


@app.route('/movie/<int:year1>/to/<int:year2>', )
def page_movies_by_years(year1, year2):
    movies = get_movies_by_release_years(year1, year2)
    return render_template('movies_by_years.html', movies=movies, year1=year1, year2=year2)


@app.route('/rating/<age>', )
def page_movies_by_age(age):
    movies = get_movies_by_age(age)

    match age:
        case 'children':
            category = "для детей"
        case 'family':
            category = "для семейного просмотра"
        case 'adult':
            category = "для взрослых"

    return render_template('movies_by_age.html', movies=movies, category=category)


@app.route('/genre/<genre>', )
def page_movies_by_genre(genre):
    movies = get_movies_by_genre(genre)
    return render_template('movies_by_genre.html', movies=movies, genre=genre)


if __name__ == '__main__':
    app.run(debug=True)
