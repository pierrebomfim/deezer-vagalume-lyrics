# Ler DB com dados da playlist e musias, requisita dados do Vagalume e salva em DB
import urllib.request, urllib.parse, urllib.error 
import json
from deezer_tk import songs
from deezer_pl import playlist_id
import sqlite3

# Para que seja impresso apenas as letras da playlist desejada
conn = sqlite3.connect('mydeezer.db')
cur = conn.cursor()

cur.execute('''SELECT id FROM Playlists WHERE id_deezer = ? ''', (playlist_id, ))
db_pl_id = cur.fetchone()[0]

cur.execute('''SELECT title, artist FROM Tracks WHERE playlists_id = ? ''', (db_pl_id, ))
songs = cur.fetchall()

for s in songs:
    song_name = s[0]
    artist_name = s[1]
    #print('dentro do loop', song_name, artist_name)

conn.commit()
cur.close()

# parse.quote to enconde a string into URL format
mus = urllib.parse.quote(song_name)
art = urllib.parse.quote(artist_name)
# Personal Key generate by myvagalume.com.br
key = '5bf325dd4cf0161ca30f8444ce58c48c'
# API url
url = f'https://api.vagalume.com.br/search.php?art={art}&mus={mus}&apikey={key}'

uh = urllib.request.urlopen(url)
data = uh.read().decode()
print("Conexão com API estabelecida!")
js = json.loads(data)

# Code to extract the lyrics from Json 
lyric = js['mus'][0]['text']
type = js['type']


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

#Se a letra estiver disponível, é adicionda ao DB. Senão, printa msg de error/not found
if type == 'exact' or type == 'aprox':
    
    cur.execute('''INSERT OR IGNORE INTO Artist (artist) VALUES ( ? )''', (artist_name, ))
    cur.execute('''SELECT id FROM Artist WHERE artist = ? ''', (artist_name, ))
    artist_id = cur.fetchone()[0]

    # Falta nalisar como pegar a tradução. Código antigo tá no arquivo teste.py !!!!!

    cur.execute('''INSERT OR IGNORE INTO Lyrics (song, lyric, artist_id) VALUES ( ?, ?, ?)''',
                (song_name, lyric, artist_id))
    print(f'Letra da música {song_name} ({artist_name}) adicionada ao Banco de Dados')
else:
    print('Song/Artist not sound!')

conn.commit()
cur.close()