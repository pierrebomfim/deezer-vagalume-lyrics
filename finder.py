from vagalume import lyrics
import sqlite3

#Criar BD MyLyrics
conn = sqlite3.connect('mylyrics')
cur = conn.cursor()

#Esse módulo é para teste. o input virá diretamente dos dados do Deezer
artist_name = input('Digite o nome do artista: ')
song_name = input('Digite o nome da música: ')

result = lyrics.find(artist_name, song_name)

if result.is_not_found():
    print('Song not sound')
else:
    print(result.song.name)
    print(result.artist.name)
    print(result.song.lyric)

    translation = result.get_translation_to('pt-br')
    if not translation:
        print('Translation not found')
    else:
        print(translation.name)
        print(translation.lyric)
