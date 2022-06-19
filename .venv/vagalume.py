# Ler DB com dados da playlist e musias, requisita dados do Vagalume e salva em DB
import urllib.request, urllib.parse, urllib.error 
import json
from deezer_tk import tracks
import sqlite3

conn = sqlite3.connect('mydeezer.db')
cur = conn.cursor()

n = 0
tracks = tracks[:3]
track_list = []
for t in tracks:
    title_track = t["title"]
    track_list.append(title_track)
    artist_track = t["artist"]["name"]
    track_list.append(title_track)
    # parse.quote to enconde a string into URL format
    mus = urllib.parse.quote(title_track)
    art = urllib.parse.quote(artist_track)
    # Personal Key generate by myvagalume.com.br
    key = '5bf325dd4cf0161ca30f8444ce58c48c'
    # API url
    url = f'https://api.vagalume.com.br/search.php?art={art}&mus={mus}&apikey={key}'
    uh = urllib.request.urlopen(url)
    data = uh.read().decode()
    #print("Conexão com API estabelecida!")
    js = json.loads(data)

    # Code to extract the lyrics from Json 
    try:
        lyric = js['mus'][0]['text']
    except:
        lyric = "Not Found"
    #print(lyric)
    type = js['type']
 
    cur.execute('''SELECT id FROM Tracks WHERE title = ? ''', (title_track, ))
    track_id = cur.fetchone()[0]
    cur.execute('''INSERT OR IGNORE INTO Lyrics (lyric, track_id) VALUES ( ?, ? )''', (lyric, track_id,))
    conn.commit()
    n = n + 1

    # Falta nalisar como pegar a tradução. Código antigo tá no arquivo teste.py !!!!!

    print(n, f'Letra da música {title_track} (artista?) adicionada ao Banco de Dados')
    
cur.close()

