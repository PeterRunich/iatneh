from ..local_libs.decorators import query_decorator
from ..local_libs.singleton import Singleton
import sqlite3
import asyncio

class Sqlite(metaclass=Singleton):
    def __init__(self):
        self.conn = sqlite3.connect("./iatneh/database/iatneh.db")
        self.cursor = self.conn.cursor()

        self.cache = {}
        self.__cache_all_genres()
        self.__cache_count_genres()

    @query_decorator
    def get_genres(self, limit, offset):
        query = f"select id, name from genres limit {limit} offset {offset}"

        if 'all_genres' in self.cache:
            return self.cache['all_genres'][offset:offset+limit], 'cached | ' + query
        else:
            return self.cursor.execute(query).fetchall(), query

    @query_decorator
    def find_genre_by_name(self, name):
        query = f"select * from genres where name like '%{name}%'"

        return self.cursor.execute(query).fetchall(), query

    @query_decorator
    def count_genres(self):
        query = f"select count(*) from genres"
        if 'count_genres' in self.cache:
            return self.cache['count_genres'], 'cached | ' + query
        else:
            return self.cursor.execute(query).fetchone()[0], query


    @query_decorator
    def find_anime_by_name(self, name, limit=0, offset=0):
        query = f"select * from animes where name like '%{name}%'"
        if limit != 0: query += f' limit {limit} offset {offset}'
        return self.cursor.execute(query).fetchall(), query

    @query_decorator
    def find_anime_by_genre(self, genres, limit=0, offset=0):
        query = "select * from animes a where "
        for genre_id in genres:
            query += f"EXISTS (SELECT * FROM animes_genres ag WHERE a.id = ag.anime_id AND ag.genre_id = {genre_id}) and "
        query = query[:-4] # удаляет не нужный and в конце запроса, он появляется из-за предыдущий строки
        if limit != 0: query += f' limit {limit} offset {offset}'

        return self.cursor.execute(query).fetchall(), query

    def __cache_all_genres(self):
        self.cache['all_genres'] = self.get_genres(limit=10000, offset=0)

    def __cache_count_genres(self):
        self.cache['count_genres'] = self.count_genres()
