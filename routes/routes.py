from flask import Blueprint, abort, redirect, render_template, url_for
from textblob import TextBlob
from forms import SearchForm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

from functions.Lyrics import getLyrics
from functions.Promedio import duration_minutes, getTrackData

routes = Blueprint("routes", __name__, template_folder="templates")

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

data = pd.DataFrame(
    columns=[
        "track_id",
        "track_name",
        "album_id",
        "artist_id",
        "lyrics",
        "polarity",
        "subjectivity",
        "danceability",
        "energy",
        "speechiness",
        "acousticness",
        "duration",
    ]
)


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
        albums += spotify.artist_albums(artist_id, album_type="single")["items"]

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
    global data
    data = data[0:0]
    artist_name = spotify.artist(artist)["name"]
    results = spotify.search(q=album + "artist:" + artist_name, type="album")
    items = results["albums"]["items"][0]

    album_id = items["id"]
    image_url = items["images"][0]["url"]
    tracks = spotify.album_tracks(album_id)["items"]

    # Análisis (Esto no debe ir aquí se quita luego)
    for track in tracks:
        insert = pd.DataFrame(
            [
                {
                    "track_id": track["id"],
                    "track_name": track["name"],
                    "album_id": album_id,
                    "artist_id": artist,
                    "lyrics": getLyrics(artist_name, track["name"]),
                    "duration": track["duration_ms"],
                }
            ]
        )

        data = pd.concat([data, insert], ignore_index=True)
        data[["polarity", "subjectivity"]] = data.lyrics.astype(str).apply(
            lambda Text: pd.Series(TextBlob(Text).sentiment)
        )

        data[
            [
                "danceability",
                "energy",
                "speechiness",
                "acousticness",
            ]
        ] = getTrackData(track["id"])

    return render_template(
        "album.html",
        album_name=album,
        artist_name=artist_name,
        tracks=tracks,
        data=data,
        image_url=image_url,
    )


@routes.route("/<string:artist>/<string:album>/<string:track>/")
def track_page(artist, album, track):
    global data

    if data.empty:
        print("error")

    artist_name = spotify.artist(artist)["name"]
    album_name = spotify.album(album)["name"]
    result = spotify.track(track)

    track_name = result["name"]
    image_url = result["album"]["images"][0]["url"]

    aux = data[data.track_id == track]
    lyrics = aux.lyrics.values[0]
    polarity = f"{aux.polarity.values[0]:.04f}"
    subjectivity = f"{aux.subjectivity.values[0]:.04f}"
    duration = duration_minutes(aux.duration.values)

    getTrackData(track)

    return render_template(
        "track.html",
        track_name=track_name,
        artist_name=artist_name,
        image_url=image_url,
        lyrics=lyrics,
        polarity=polarity,
        subjectivity=subjectivity,
        duration=duration,
    )
