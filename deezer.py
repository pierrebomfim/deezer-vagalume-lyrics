import sqlite3

# Criar BD MyLyrics
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