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
album_name = input("Ingresa el nombre del álbum: ")

# Obtener el ID del artista
results = spotify.search(q='artist:' + artist_name, type='artist')
items = results['artists']['items']
if len(items) > 0:
    artist_id = items[0]['id']

    # Obtener los álbumes del artista
    albums = spotify.artist_albums(artist_id, album_type='album')['items']

    # Buscar el ID del álbum deseado
    album_id = None
    for album in albums:
        if album['name'] == album_name:
            album_id = album['id']
            break

    if album_id:
        # Obtener álbum
        tracks = spotify.album_tracks(album_id)['items']

        # Imprimir canciones
        print(f"Canciones del álbum '{album_name}':")
        for track in tracks:
            print(track['name'])
    else:
        print(f"No se encontró el álbum '{album_name}' para el artista '{artist_name}'.")
else:
    print(f"No se encontró al artista '{artist_name}'.")
