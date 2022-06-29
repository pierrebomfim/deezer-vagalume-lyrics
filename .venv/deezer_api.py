from http.client import ImproperConnectionState
import urllib.request
import urllib.parse
import urllib.error
import json
import sqlite3

from requests import get


'''Criação do Banco de Dados mydeezer.'''
conn = sqlite3.connect('mydeezer.db')
cur = conn.cursor()

cur.execute('''
            CREATE TABLE IF NOT EXISTS Playlists
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, id_deezer INTEGER, title TEXT UNIQUE, nb_tracks INTEGER);
''')

cur.execute('''
            CREATE TABLE IF NOT EXISTS Tracks 
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, id_deezer INTEGER, title TEXT UNIQUE, artist TEXT, album TEXT, playlist_id INTEGER);
''')

cur.execute('''
            CREATE TABLE IF NOT EXISTS Lyrics
            (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, lyric TEXT UNIQUE, track_id INTEGER);
''')

conn.commit()


def get_user_playlists():
    '''Requisita json do Deezer e retorna Json com dados do user.'''
    user = input('Enter your Deezer ID: ')
    url = f'http://api.deezer.com/user/{user}/playlists'
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    js = json.loads(data)
    print('getplaylists()')
    return js

user_playlists = get_user_playlists()

def show_playlists(user_playlists):
    '''Abre o Json, lista as playlists e retorna um dict com dados do Json.'''
    #playlists_json = get_user_playlists()
    playlists = user_playlists['data']
    playlist_list = []
    for p in playlists:
        playlist_name = p['title']
        #nb_tracks = p['nb_tracks']
        playlist_list.append(playlist_name)
    print(playlist_list)
    print('show_playlists()')
    return playlists

playlists = show_playlists(user_playlists)

def choose_playlist(playlists):
    '''Escolher a playlista e retornar o seu id'''
    #print(playlists)
    playlist_input = input("Enter playlist's name: ")
    playlist_choosen = next((x for x in playlists if x['title'] == playlist_input), None)
    playlist_id = playlist_choosen['id']
    print('choose_playlists()')
    return playlist_id

playlist_id = choose_playlist(playlists)

def get_playlist_data(playlist_id):
    '''Requista Json da API específica da playlista escolhida. Salva dados no DB'''
    #id = choose_playlist()
    url = f'http://api.deezer.com//playlist//{playlist_id}'
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    js = json.loads(data)
    title = js['title']
    nb_tracks = js['nb_tracks']
    cur.execute('''
                INSERT OR IGNORE INTO Playlists
                (id_deezer, title, nb_tracks) VALUES (?, ?, ?)''',
                (playlist_id, title, nb_tracks)
    )
    print('get_playlist_data')
    conn.commit()
    return js

playlist_data = get_playlist_data(playlist_id)


def get_save_tracks(playlist_data):
    ''' Do Json, retira informações das músicas e salva em DB.'''
    js = playlist_data
    pl_id = js['id']
    tracks = js['tracks']['data']
    for t in tracks:
        id = t['id']
        title = t['title']
        artist = t['artist']['name']
        album = t['album']['title']

        ''' Inserir dados na tabela Tracks no DB'''
        cur.execute('''
                    INSERT OR IGNORE INTO Tracks 
                    (id_deezer, title, artist, album, playlist_id) VALUES ( ?, ?, ?, ?, ?)''',
                    (id, title, artist, album, pl_id)
        )
        conn.commit()
    print('get_save_tracks')
    #return pl_id


# VAGALUME API

def get_track_data(playlist_id):
    ''' Ler as músicas no DB, encoda os dados, requisita a letra no API Vagalume e salva no DB'''
    #id = get_save_tracks()

    cur.execute('''
                SELECT title, artist FROM Tracks WHERE playlist_id = ? ''',
                (playlist_id,)
    )
    tracks = cur.fetchall()
    conn.commit()
    print('get_track_data')

    for t in tracks:
        #print(t[0], t[1])
        title = urllib.parse.quote(t[0])
        artist = urllib.parse.quote(t[1])
        url = f'https://api.vagalume.com.br/search.php?art={artist}&mus={title}&apikey=5bf325dd4cf0161ca30f8444ce58c48c'
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        js = json.loads(data)

        try:
            lyric = js['mus'][0]['text']
        except:
            lyric = 'Not found - Não encontrado'
        
        cur.execute('''
                    SELECT id_deezer FROM Tracks WHERE title = ?''', (t[0],)
        )
        id = cur.fetchone()[0]
        conn.commit()
        cur.execute('''
                    INSERT OR IGNORE INTO Lyrics (lyric, track_id) VALUES ( ?, ?)''', (lyric, id)
        )
        conn.commit()

    print("ok")        

    #return tracks


get_save_tracks(playlist_data)
get_track_data(playlist_id)

#def vagalume_api():
 #   'Requisita a letra da API Vagalume.'

conn.close()

'''
JÁ ESTÁ FUNCIONANDO CORRETAMENTE!!!! FALTA INTEGRAR COM O GERADOR DE PDF!!!
*ESTAVA COM DIFICULDADES DE TESTAR, DEVIDO Á INTERNET RUIM
'''


