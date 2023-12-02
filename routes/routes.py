from flask import Blueprint, redirect, render_template, url_for
from forms import SearchForm
import pandas as pd

from functions.Analisis import album_analisis, track_analisis
from functions.Promedio import duration_minutes
from functions.Spotify import spotify

routes = Blueprint("routes", __name__, template_folder="templates")

data = pd.DataFrame()


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

    data = album_analisis(tracks, album_id, artist, data)

    return render_template(
        "album.html",
        album_name=album,
        artist_name=artist_name,
        data=data,
        image_url=image_url,
    )


@routes.route("/<string:artist>/<string:album>/<string:track>/")
def track_page(artist, album, track):
    global data

    artist_name = spotify.artist(artist)["name"]
    album_name = spotify.album(album)["name"]
    result = spotify.track(track)
    image_url = result["album"]["images"][0]["url"]

    if data.empty or not track in data.track_id.values:
        data = track_analisis(track, album, artist, data)

    aux = data[data.track_id == track].iloc[0]
    polarity = f"{aux.polarity:.04f}"
    subjectivity = f"{aux.subjectivity:.04f}"
    duration = duration_minutes(aux.duration)

    return render_template(
        "track.html",
        data=aux,
        artist_name=artist_name,
        image_url=image_url,
        duration=duration,
        polarity=polarity,
        subjectivity=subjectivity,
    )
