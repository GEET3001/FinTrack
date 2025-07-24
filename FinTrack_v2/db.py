import streamlit as st
import pymysql
from pymysql.cursors import DictCursor

class Database:
    def __init__(self):
        creds = st.secrets["mysql"]
        self.connection = pymysql.connect(
            host=creds["host"],
            user=creds["user"],
            password=creds["password"],
            database=creds["database"],
            cursorclass=DictCursor,
            charset='utf8mb4'
        )

    def execute(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            self.connection.commit()
            return cursor

    def fetchone(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchone()

    def fetchall(self, query, params=None):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

    def close(self):
        self.connection.close()
