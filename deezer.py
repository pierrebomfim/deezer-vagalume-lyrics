import sqlite3
from tracks import musicas

print(musicas)

# Criar BD My Deezer
conn = sqlite3.connect('mydeezer.db')
cur = conn.cursor()

cur.execute('''
            CREATE TABLE IF NOT EXISTS Artist
            (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, artist TEXT);
            ''')

cur.execute('''
            CREATE TABLE IF NOT EXISTS Translation
            (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, letra TEXT);
            ''')

cur.execute('''
            CREATE TABLE IF NOT EXISTS Lyrics
            (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, song TEXT, lyric TEXT, artist_id INTEGER, translation_id INTERGER);
            ''')

#playlist = input('Digite a playlist que deseja pesquisar: ')
