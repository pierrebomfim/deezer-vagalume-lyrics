'''
Recebe o id da playlist de xxxxxx, requisita dados da playlist e extrai as músicas.
'''

from http.client import ImproperConnectionState
import urllib.request, urllib.parse, urllib.error
import json
from teste import playlist_id

#url = f'http://api.deezer.com//playlist//{playlist_id}'  for test
if playlist_id == 9287938602:
    url = 'file:///C:/Users/pierr/OneDrive/Desktop/Deezer%20API/9287938602.json'

uh = urllib.request.urlopen(url)
data = uh.read().decode()

js = json.loads(data)

print('Playlist: ', js["title"])
print('ID: ', playlist_id)

tracks = js["tracks"]["data"]
print('Músicas: ')
n = 0 
for t in tracks:
    n = n + 1
    songs = t["title"]
    artist = t["artist"]["name"]
    print(n, songs, f'({artist})')