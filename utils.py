import sqlite3
from collections import Counter

DATA = 'netflix.db'


def db_connect(db, query):
    """
    Подключение к БД и получение списка данных по заданным параметрам.
    :param db: база данных.
    :param query: параметры запроса.
    :return: результат отбора.
    """
    with sqlite3.connect(db) as con:
        cur = con.cursor()
        cur.execute(query)
        result = cur.fetchall()
        return result


def get_movie_by_id(movie_title):
    """
    Находит фильм по названию.
    :param movie_title: название фильма (или слово в названии).
    :return: первый фильм из списка найденных.
    """
    query = f"""SELECT title, country, release_year, listed_in, description FROM netflix
         WHERE type = 'Movie' AND title like '%{movie_title}%'
         ORDER BY release_year DESC 
         LIMIT 1
         """
    movie = db_connect(DATA, query)
    if movie:
        found_movie = {
            "title": movie[0][0],
            "country": movie[0][1],
            "release_year": movie[0][2],
            "genre": movie[0][3],
            "description": movie[0][4].rstrip('\n')
        }
        print(found_movie)
        return found_movie
    else:
        return "Movies not found"


def get_movies_by_release_years(start_year, end_year):
    """
    Выводит список фильмов по диапазону дат выхода.
    :param start_year: год начала поиска.
    :param end_year: последний год из диапазона поиска.
    :return: список фильмов, входящих в диапазон, ограниченный 100 первыми фильмами.
    """
    selected_movies = []
    query = f"""SELECT title, release_year
                FROM netflix
                WHERE release_year BETWEEN {start_year} AND {end_year}
                ORDER BY release_year
                LIMIT 100;
            """
    movies = db_connect(DATA, query)

    for movie in movies:
        selected_movies.append({
            "title": movie[0],
            "release_year": movie[1],
        })
    return selected_movies


def get_movies_by_age(age):
    """
    Сортирует фильмы в зависимости от возрастных ограничений.
    :param age: возрастная категория.
    :return: список фильмов, соответствующий категории.
    """
    selected_movies = []
    age_category = get_age_category(age)

    query = f"""SELECT title, rating, description
                FROM netflix
                WHERE rating IN ('{age_category}')
                ORDER BY title
                LIMIT 100;
            """
    movies = db_connect(DATA, query)

    for movie in movies:
        selected_movies.append({
            "title": movie[0],
            "rating": movie[1],
            "description": movie[2].rstrip('\n'),
        })
    return selected_movies


def get_age_category(age):
    """
    Возвращает список обозначений возрастных категорий и преобразует его к строке.
    :param age: возрастная категория зрителей.
    :return: строка, содержащая возрастные категории, соответствующие обозначениям в БД Netflix.
    """
    if age.lower() == 'children':
        age_category = ['G']
    elif age.lower() == 'family':
        age_category = ['G', 'PG', 'PG-13']
    elif age.lower() == 'adult':
        age_category = ['R', 'NC-17']
    else:
        return "Уточните категорию"

    if len(age_category) > 1:
        str_age_category = "','".join(age_category)
    else:
        str_age_category = "".join(age_category)

    return str_age_category


def get_movies_by_genre(genre):
    """
    Формирует список из 10 самых свежих фильмов, соответствующих искомому жанру.
    :param genre: жанр фильма.
    :return: список отобранных фильмов.
    """
    selected_movies = []

    query = f"""SELECT title, listed_in, description
                   FROM netflix
                   WHERE listed_in LIKE '%{genre}%'
                   ORDER BY release_year DESC
                   LIMIT 10;
               """
    movies = db_connect(DATA, query)

    for movie in movies:
        selected_movies.append({
            "title": movie[0],
            "description": movie[2].rstrip('\n'),
        })
    return selected_movies


def get_actors(first_actor, second_actor):
    """
    Формирует список актёров, играющих с заданными, более, чем в двух фильмах.
    :param first_actor: первый актёр.
    :param second_actor: второй актёр.
    :return: список отобранных актёров.
    """
    all_actors = []
    selected_actors = []

    query = f"""SELECT netflix.cast
                      FROM netflix
                      WHERE netflix.cast LIKE '%{first_actor}%' AND netflix.cast LIKE '%{second_actor}%';
                  """
    result = db_connect(DATA, query)

    for actors in result:
        actors_list = actors[0].split(',')
        all_actors += actors_list
    counter = Counter(all_actors)
    for key, value in counter.items():
        if value > 2 and key.strip() not in [first_actor, second_actor]:
            selected_actors.append(key)
    return selected_actors


def get_movies_list(type_, year, genre):
    """
    Формирует список фильмов, соответствующих искомому типу, году выпуска и жанру.
    :param type_: тип (фильм или шоу/сериал).
    :param year: год выпуска.
    :param genre: жанр.
    :return: список отобранных фильмов с описаниями.
    """
    result_list = []

    query = f"""SELECT type, title, release_year, listed_in, description 
                        FROM netflix
                        WHERE type LIKE '%{type_}%' 
                        AND release_year = {year} 
                        AND listed_in LIKE '%{genre}%';
                    """
    result = db_connect(DATA, query)

    for row in result:
        result_list.append({
            "type": row[0],
            "title": row[1],
            "year": row[2],
            "genre": row[3],
            "description": row[4],
        })

    return result_list
