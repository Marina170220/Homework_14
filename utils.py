import json
import sqlite3


def get_movie_by_id(movie_title):
    """
    Находит фильм по названию.
    :param movie_title: название фильма (или слово в названии).
    :return: первый фильм из списка найденных.
    """
    selected_movies = []
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = ("SELECT * FROM netflix"
                        " WHERE type = 'Movie' "
                        "ORDER BY release_year DESC ")
        cur.execute(sqlite_query)
        executed_query = cur.fetchall()

        for row in executed_query:
            if movie_title.lower() in row[2].lower():
                found_movie = {
                    "title": row[2],
                    "country": row[5],
                    "release_year": row[7],
                    "genre": row[8],
                    "description": row[12]
                }
                selected_movies.append(found_movie)
        return selected_movies[0]


def get_movies_by_release_years(start_year, end_year):
    """
    Выводит список фильмов по диапазону дат выхода.
    :param start_year: год начала поиска.
    :param end_year: последний год из диапазона поиска.
    :return: список фильмов, входящих в диапазон, ограниченный 100 первыми фильмами.
    """
    selected_movies = []
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = ("SELECT title, release_year FROM netflix "
                        "WHERE type = 'Movie' "
                        "ORDER BY release_year "
                        )
        cur.execute(sqlite_query)
        executed_query = cur.fetchall()

        for row in executed_query:
            if start_year <= row[1] <= end_year:
                selected_movies.append({
                    "title": row[0],
                    "release_year": row[1],
                })
        return selected_movies[:100]


def get_movies_by_age(age_category):
    """
    Сортирует фильмы в зависимости от возрастных ограничений.
    :param age_category: возрастная категория.
    :return: список фильмов, соответствующий категории.
    """
    movies_for_children = []
    movies_for_family = []
    movies_fo_adults = []

    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = ("SELECT title, rating, description FROM netflix "
                        "WHERE type = 'Movie' "
                        "ORDER BY rating ")
        cur.execute(sqlite_query)
        executed_query = cur.fetchall()

        for row in executed_query:
            if row[1] == 'G':
                movies_for_children.append({
                    "title": row[0],
                    "rating": row[1],
                    "description": row[2],
                })

            elif row[1] in ['G', 'PG', 'PG-13']:
                movies_for_family.append({
                    "title": row[0],
                    "rating": row[1],
                    "description": row[2],
                })

            elif row[1] in ['R', 'NC-17']:
                movies_fo_adults.append({
                    "title": row[0],
                    "rating": row[1],
                    "description": row[2],
                })

        match age_category:
            case 'children':
                return movies_for_children
            case 'family':
                return movies_for_family
            case 'adult':
                return movies_fo_adults


def get_movies_by_genre(genre):
    """
    Формирует список из 10 самых свежих фильмов, соответствующих искомому жанру.
    :param genre: жанр фильма.
    :return: список отобранных фильмов.
    """
    selected_movies = []
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = ("SELECT title, listed_in, description FROM netflix "
                        "WHERE type = 'Movie' "
                        "ORDER BY release_year DESC "
                        )
        cur.execute(sqlite_query)
        executed_query = cur.fetchall()

        for row in executed_query:
            if genre.lower() in row[1].lower():
                selected_movies.append({
                    "title": row[0],
                    "description": row[2],
                })
        return selected_movies[:10]


def get_actors(first_actor, second_actor):
    """
    Формирует список актёров, играющих с заданными, более, чем в двух фильмах.
    :param first_actor: первый актёр.
    :param second_actor: второй актёр.
    :return: список отобранных актёров.
    """
    actors = []
    selected_actors = set()
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = ("SELECT netflix.cast FROM netflix "
                        "WHERE type = 'Movie' ")
        cur.execute(sqlite_query)
        executed_query = cur.fetchall()

        for row in executed_query:
            if first_actor and second_actor in row[0]:
                for actor in row[0].split(', '):
                    if actor != first_actor and actor != second_actor:
                        actors.append(actor)
                        if actors.count(actor) >= 2:
                            selected_actors.add(actor)

        return selected_actors


def get_movies_list(type_, year, genre):
    """
    Формирует список фильмов, соответствующих искомому типу, году выпуска и жанру.
    :param type_: тип (фильм или шоу/сериал).
    :param year: год выпуска.
    :param genre: жанр.
    :return: список отобранных фильмов с описаниями.
    """
    movies = []
    tv_shows = []
    with sqlite3.connect("netflix.db") as con:
        cur = con.cursor()
        sqlite_query = ("SELECT type, title, release_year, listed_in, description "
                        "FROM netflix "
                        "WHERE type != '' ")
        cur.execute(sqlite_query)
        executed_query = cur.fetchall()

        for row in executed_query:
            if row[0] == 'Movie':
                movies.append({
                    "title": row[1],
                    "year": row[2],
                    "genre": row[3],
                    "description": row[4],
                })
            else:
                tv_shows.append({
                    "title": row[1],
                    "year": row[2],
                    "genre": row[3],
                    "description": row[4],
                })

        if type_.lower() == 'movie':
            found_movies = [movie for movie in movies if year == movie.get('year')
                            and genre.lower() in movie.get("genre").lower()]

        else:
            found_movies = [show for show in tv_shows if year == show.get('year')
                            and genre.lower() in show.get("genre").lower()]

        return found_movies


# """
# Проверка записи в json-файл
# """
# with open('movies.json', 'w',  encoding='UTF-8') as fp:
#     movies = get_movies_list('Movie', 2010, 'dramas')
#     json.dump(movies, fp, indent=4)

