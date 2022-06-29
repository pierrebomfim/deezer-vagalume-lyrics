import sqlite3
import

def get_track_data(playlist_id):
    ''' Ler as músicas no DB e requisita a letra no API Vagalume.'''
    #id = get_save_tracks()

    cur.execute('''
                SELECT title, artist FROM Tracks WHERE playlist_id = ? ''',
                (playlist_id,)
    )
    title = cur.fetchall()[0]
    artist = cur.fetchall()
    conn.commit()
    print(playlist_id)
    print('get_track_data')
    print(title, artist)
    #return tracks

get_save_tracks(playlist_data)
get_track_data(playlist_id)