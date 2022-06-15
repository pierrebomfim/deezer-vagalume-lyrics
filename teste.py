from http.client import ImproperConnectionState
import urllib.request, urllib.parse, urllib.error
import json

#url = 'http://api.deezer.com/user/1747640386/playlists' Para teste
url = 'file:///C:/Users/pierr/OneDrive/Desktop/Deezer%20API/playlists.json'

uh = urllib.request.urlopen(url)
data = uh.read().decode()

js = json.loads(data)

plquery = input("Digite o nome da playlist: ")
if len(plquery) < 1:  # Para teste
    plquery = "Ir. kelly Patricia"
playlists_deezer = js["data"]
playlist = next((x for x in playlists_deezer if x["title"] == plquery), None)
playlist_id = playlist['id']
