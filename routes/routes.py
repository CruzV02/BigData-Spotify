from flask import Blueprint, abort, redirect, render_template, url_for
from forms import SearchForm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

from functions.Lyrics import getLyrics

routes = Blueprint("routes", __name__, template_folder="templates")

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

data = pd.DataFrame(columns=["track_id", "artist_id", "album_id", "lyrics"])


@routes.route("/", methods=["POST", "GET"])
def index():
    form = SearchForm()
    error = None
    if form.validate_on_submit():
        artist = form.artist.data
        return redirect("/" + artist + "/")
    
    return render_template("index.html", form=form, error=error)


@routes.route("/<string:artist>/")
def artist_page(artist):
    results = spotify.search(q="artist:" + artist, type="artist")

    if results["artists"]["total"] < 1:
        print("Error")
        return redirect(url_for("routes.index"))
        # abort(404)
    else:
        items = results["artists"]["items"]

        artist_id = items[0]["id"]
        artist_name = items[0]["name"]
        image_url = items[0]["images"][0]["url"]
        albums = spotify.artist_albums(artist_id, album_type="album")["items"]
        # albums += spotify.artist_albums(artist_id, album_type="single")["items"]

        # Análisis TopTen
        """
        top_ten = spotify.artist_top_tracks(artist_id)["tracks"]
        lyrics = []
        for track in top_ten:
            print(track["name"])
            lyrics += getLyrics(artist_name, track["name"])
        """

    return render_template(
        "artist.html",
        artist_id=artist_id,
        artist_name=artist_name,
        albums=albums,
        image_url=image_url,
    )


@routes.route("/<string:artist>/<string:album>/")
def album_page(artist, album):
    artist_name = spotify.artist(artist)["name"]
    results = spotify.search(q=album + "artist:" + artist_name, type="album")
    items = results["albums"]["items"][0]

    album_id = items["id"]
    image_url = items["images"][0]["url"]
    tracks = spotify.album_tracks(album_id)["items"]

    return render_template(
        "album.html",
        album_id=album_id,
        album_name=album,
        artist_name=artist_name,
        artist_id=artist,
        tracks=tracks,
        image_url=image_url,
    )


@routes.route("/<string:artist>/<string:album>/<string:track>/")
def track_page(artist, album, track):
    artist_name = spotify.artist(artist)["name"]
    album_name = spotify.album(album)["name"]

    results = spotify.search(
        q=track + "album:" + album_name + "artist:" + artist_name, type="track"
    )
    items = results["tracks"]["items"][0]
    print(items)

    track_name = items["name"]
    image_url = items["album"]["images"][0]["url"]

    return render_template(
        "track.html",
        track_name=track_name,
        artist_name=artist_name,
        image_url=image_url,
    )
