# Requisita dados do deezer e da playlist desejada

from http.client import ImproperConnectionState
import urllib.request
import urllib.parse
import urllib.error
import json

usuario = input('Digite o ID do seu perfil DEEZER: ')
if len(usuario) < 1:
    url = 'file:///C:/Users/pierr/OneDrive/Desktop/Deezer%20API/playlists.json'
else:
    url = f'http://api.deezer.com/user/{usuario}/playlists'
print('\nConectando à Deezer...\n')

uh = urllib.request.urlopen(url)
data = uh.read().decode()
js = json.loads(data)
#print('Retrived! Usuário Encontrado')

#print('Perfil: aqui vai o perfil, mas tem q pegar em outro link, no geral do deezer')
print('Playlists: ')
playlists = js["data"]
for p in playlists:
    pl_name = p["title"]
    n_tracks = p["nb_tracks"]
    print(pl_name, f' - {n_tracks} músicas')
print('\n')
plquery = input("Digite o nome da playlist: ")
if len(plquery) < 1:  # Para teste
    plquery = "Ir. kelly Patricia"

# Econtrar o ID da playlist desejada
playlists_deezer = js["data"]
playlist = next((x for x in playlists_deezer if x["title"] == plquery), None)
playlist_id = playlist['id']



