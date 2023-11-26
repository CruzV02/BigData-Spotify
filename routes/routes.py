from flask import Blueprint, render_template
from functions.Lyrics import getLyrics
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from textblob import TextBlob

routes = Blueprint("routes", __name__, template_folder="templates")

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

artist_name = input("Ingresa el nombre del artista: ")
album_name = input("Ingresa el nombre del álbum: ")

# Obtener el ID del artista
results = spotify.search(q="artist:" + artist_name, type="artist")
items = results["artists"]["items"]
if len(items) > 0:
    artist_id = items[0]["id"]

    # Obtener los álbumes del artista
    albums = spotify.artist_albums(artist_id, album_type="album")["items"]

    # Buscar el ID del álbum deseado
    album_id = None
    for album in albums:
        if album["name"] == album_name:
            album_id = album["id"]
            break

    if album_id:
        # Obtener álbum
        tracks = spotify.album_tracks(album_id)["items"]


def get_album_image_url(artist_name, album_name):
    results = spotify.search(q="artist:" + artist_name, type="artist")
    items = results["artists"]["items"]
    if len(items) > 0:
        artist = items[0]

        # Obtener los álbumes del artista
        albums = spotify.artist_albums(artist["id"], album_type="album")["items"]

        # Buscar el ID del álbum deseado
        album_id = None
        for album in albums:
            if album["name"] == album_name:
                album_id = album["id"]
                break

        if album_id:
            # Obtener álbum
            album = spotify.album(album_id)
            return album["images"][0]["url"]

    return None


@routes.route("/")
def index():
    tracks = spotify.album_tracks(album_id)["items"]
    lyrics = []
    for track in tracks:
        lyrics.append(getLyrics(artist_name, track["name"]))
        print(track["name"])

    data = pd.DataFrame(lyrics, columns=["lyrics", "para"])
    data.lyrics = data.lyrics.astype(str)
    data[["polarity", "subjectivity"]] = data["lyrics"].apply(
        lambda Text: pd.Series(TextBlob(Text).sentiment)
    )
    print(data.head())

    image_url = get_album_image_url(artist_name, album_name)
    return render_template(
        "canciones.html",
        artist_name=artist_name,
        album_name=album_name,
        tracks=tracks,
        image_url=image_url,
        lyrics=lyrics,
    )
