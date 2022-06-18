# Ler DB com dados da playlist e musias, requisita dados do Vagalume e salva em DB
from vagalume import lyrics
from deezer_tk import songs
from deezer_pl import playlist_id
import sqlite3

# Esse módulo é para teste. o input virá diretamente dos dados do Deezer
#artist_name = input('Digite o nome do artista: ')
#song_name = input('Digite o nome da música: ')

# 1 Com esse código, o dados vem do JSON
'''
artist_name = artist
song_name = songs
'''
# 2 - Com esse, o dado vem do DB
conn_mydeezer = sqlite3.connect('mydeezer.db')
cur_mydeezer = conn_mydeezer.cursor()

    # Para que seja impresso apenas as letras da playlist desejada
cur_mydeezer.execute('''SELECT id FROM Playlists WHERE id_deezer = ? ''', (playlist_id, ))
db_pl_id = cur_mydeezer.fetchone()[0]

cur_mydeezer.execute('''SELECT title, artist FROM Tracks WHERE playlists_id = ? ''', (db_pl_id, ))
songs = cur_mydeezer.fetchall()

for s in songs:
    song_name = s[0]
    artist_name = s[1]
    print(song_name, artist_name)

conn_mydeezer.commit()
cur_mydeezer.close()

# Criar BD MyLyrics
conn = sqlite3.connect('mylyrics.db')
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
conn.commit()
cur.close()

result = lyrics.find(artist_name, song_name)

if result.is_not_found():
    print('Song not sound!')
else:
    print('Música: ', result.song.name)
    print('Artista: ', result.artist.name)

    lyric = result.song.lyric

    cur.execute(
        '''INSERT OR IGNORE INTO Artist (artist) VALUES ( ? )''', (artist_name, ))
    cur.execute('''SELECT id FROM Artist WHERE artist = ? ''', (artist_name, ))
    artist_id = cur.fetchone()[0]

    translation = result.get_translation_to('pt-br')
    if not translation:
        print('Translation not found')
    else:
        cur.execute('''INSERT OR IGNORE INTO Translation (letra) VALUES ( ? )''',
                    (translation.lyric, ))
        cur.execute('''SELECT id FROM Translation WHERE letra = ? ''',
                    (translation.lyric, ))
        translation_id = cur.fetchone()[0]
        print('A tradução foi salva no banco de dados')

    cur.execute('''INSERT OR IGNORE INTO Lyrics (song, lyric, artist_id, translation_id) VALUES ( ?, ?, ?, ? )''',
                (song_name, lyric, artist_id, translation_id))

    print('A letra foi salva no Bando de Dados!')

# Como fazer com que um artista com mais de uma música não se repita na tabela artist ???
