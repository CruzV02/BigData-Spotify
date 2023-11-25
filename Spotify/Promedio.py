import spotipy
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configurar las credenciales de Spotify
os.environ["SPOTIPY_CLIENT_ID"] = os.getenv("SPOTIPY_CLIENT_ID")
os.environ["SPOTIPY_CLIENT_SECRET"] = os.getenv("SPOTIPY_CLIENT_SECRET")
os.environ["SPOTIPY_REDIRECT_URI"] = os.getenv("SPOTIPY_REDIRECT_URI")

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

artist_name = input("Ingresa el nombre del artista: ")

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

        # Promedio del álbum en minutos
        if total_tracks_album > 0:
            average_duration_seconds = total_duration_album / total_tracks_album / 1000
            average_duration_minutes = average_duration_seconds / 60
            print(f"Duración promedio del álbum '{album_name}': {average_duration_minutes:.2f} minutos")

        total_duration_all += total_duration_album
        total_tracks_all += total_tracks_album

    # Promedio todas las canciones en minutos
    if total_tracks_all > 0:
        average_duration_seconds_all = total_duration_all / total_tracks_all / 1000
        average_duration_minutes_all = average_duration_seconds_all / 60
        print(f"Duración promedio de todas las canciones: {average_duration_minutes_all:.2f} minutos")
    else:
        print("No se encontraron pistas para calcular el promedio final.")
else:
    print(f"No se encontró al artista '{artist_name}'.")
