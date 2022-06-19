#Recebe o id da playlist de deezer_pl.py, requisita dados da playlist e extrai as músicas. Salva em DB

from http.client import ImproperConnectionState
import urllib.request
import urllib.parse
import urllib.error
import json
from deezer_pl import playlist_id
import sqlite3

# Criar BD My Deezer
conn = sqlite3.connect('mydeezer.db')
cur = conn.cursor()

cur.execute('''
            CREATE TABLE IF NOT EXISTS Playlists
            (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, id_deezer INTEGER, title TEXT, public INTEGER, is_loved_track INTEGER, collaborative INTEGER, nb_tracks INTEGER, creator TEXT);
            ''')

cur.execute('''
            CREATE TABLE IF NOT EXISTS Tracks
            (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, id_deezer INTEGER, title TEXT, explicit_lyrics INTEGER, artist TEXT, album TEXT, playlists_id INTEGER);
            ''')

cur.execute('''
            CREATE TABLE IF NOT EXISTS Lyrics
            (id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, lyric TEXT, track_id INTEGER);
            ''')
conn.commit()

#API Deezer
# url = f'http://api.deezer.com//playlist//{playlist_id}'  for test
if playlist_id == 9287938602:
    url = 'file:///C:/Users/pierr/OneDrive/Desktop/Deezer%20API/9287938602.json'
#print("Aguarde! Conectando à API Deezer...")
uh = urllib.request.urlopen(url)
data = uh.read().decode()
js = json.loads(data)
#print("Conexão com API estabelecida!")

# Apenas para print de teste
'''
print('Playlist: ', js["title"])
print('ID: ', playlist_id)
tracks = js["tracks"]["data"]
print('Músicas: ')
n = 0
for t in tracks:
    n = n + 1
    songs = t["title"]
    artist = t["artist"]["name"]
    #print(n, songs, f'({artist})')
'''
#playlist's data
title = js["title"]
public = js["public"]
is_loved = js["is_loved_track"]
collaborative = js["collaborative"]
nb_tracks = js["nb_tracks"]
creator = js["creator"]["name"]

#Inserir dados na tabela Playlists
cur.execute(
        '''INSERT OR IGNORE INTO Playlists (id_deezer, title, public, is_loved_track, collaborative, nb_tracks, creator) VALUES ( ?, ?, ?, ?, ?, ?, ? )''', (playlist_id, title, public, is_loved, collaborative, nb_tracks, creator))
#print("Dados da playlist adicionado no DB")

#Tracks's Data
tracks_list = []
tracks = js["tracks"]["data"]
for t in tracks:
    id_track_deezer = t["id"]
    title_track = t["title"]
    tracks_list.append(title_track)
    explicit_lyrics = t["explicit_lyrics"]
    artist_track = t["artist"]["name"]
    album_track = t["album"]["title"]
    #Pegar o id na tabela playlist, para correlacionar com a tabela tracks ( id auto com id deezer)
    cur.execute('''SELECT id FROM Playlists WHERE id_deezer = ? ''', (playlist_id, ))
    pl_id = cur.fetchone()[0]
    conn.commit()

    #Inserir dados na tabela Tracks
    cur.execute(
            '''INSERT OR IGNORE INTO Tracks (id_deezer, title, explicit_lyrics, artist, album, playlists_id) VALUES ( ?, ?, ?, ?, ?, ?)''', (id_track_deezer, title_track, explicit_lyrics, artist_track, album_track, pl_id))
    conn.commit()
#print("Dados das músicas adicionados ao DB")

cur.close()