from functions.Spotify import spotify

def getTrackData(track_id):
    data = spotify.audio_features(track_id)[0]
    return (
        data["danceability"],
        data["energy"],
        data["speechiness"],
        data["acousticness"],
    )


def duration_minutes(duration_ms):
    duration_sec, duration_ms = divmod(int(duration_ms), 1000)
    duration_min, duration_sec = divmod(int(duration_sec), 60)
    return f"{duration_min:02d}:{duration_sec:02d}"


"""
# Busca al artista
results = spotify.search(q='artist:' + artist_name, type='artist')
items = results['artists']['items']

if len(items) > 0:
    # Obtiene el ID del primer artista encontrado
    artist_id = items[0]['id']

    # Obtiene la lista de álbumes del artista
    albums = spotify.artist_albums(artist_id, album_type='album')['items']

    total_duration_all = 0
    total_tracks_all = 0
    total_albums = len(albums)
    total_tracks = 0

    # Itera sobre cada álbum
    for album in albums:
        album_id = album['id']
        album_name = album['name']

        # Obtiene la lista de pistas del álbum
        tracks = spotify.album_tracks(album_id)['items']

        total_duration_album = 0
        total_tracks_album = 0

        # Itera sobre cada pista y suma la duración
        for track in tracks:
            total_duration_album += track['duration_ms']
            total_tracks_album += 1

        # Promedio del álbum en minutos y segundos
        if total_tracks_album > 0:
            average_duration_seconds = total_duration_album / total_tracks_album / 1000
            average_minutes, average_seconds = divmod(average_duration_seconds, 60)
            print(f"Duración promedio del álbum '{album_name}': {int(average_minutes):02d}:{int(average_seconds):02d} minutos")

        total_duration_all += total_duration_album
        total_tracks_all += total_tracks_album
        total_tracks += len(tracks)

    # Promedio todas las canciones en minutos y segundos
    if total_tracks_all > 0:
        average_duration_seconds_all = total_duration_all / total_tracks_all / 1000
        average_minutes_all, average_seconds_all = divmod(average_duration_seconds_all, 60)
        print(f"Duración promedio de todas las canciones: {int(average_minutes_all):02d}:{int(average_seconds_all):02d} minutos")
    else:
        print("No se encontraron pistas para calcular el promedio final.")

    # Muestra el número total de álbumes y pistas
    print(f"\nNúmero total de álbumes: {total_albums}")
    print(f"Número total de pistas: {total_tracks}")

else:
    print(f"No se encontró al artista '{artist_name}'.")
"""
