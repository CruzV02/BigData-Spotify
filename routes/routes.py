from flask import Blueprint, abort, redirect, render_template, url_for
from forms import SearchForm
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

routes = Blueprint("routes", __name__, template_folder="templates")

spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())


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
        return redirect(url_for("index"))
        # abort(404)
    else:
        items = results["artists"]["items"]

        print(items[0])

        artist_id = items[0]["id"]
        artist_name = items[0]["name"]
        image_url = items[0]["images"][0]["url"]
        albums = spotify.artist_albums(artist_id, album_type="album")["items"]
        albums += spotify.artist_albums(artist_id, album_type="single")["items"]
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
    items = results["albums"]["items"]
    print(items[0])

    album_id = items[0]["id"]
    image_url = items[0]["images"][0]["url"]
    tracks = spotify.album_tracks(album_id)["items"]
    return render_template(
        "album.html",
        album_id=album_id,
        album_name=album,
        tracks=tracks,
        image_url=image_url,
    )


@routes.route("/<string:artist>/<string:album>/<string:track>/")
def track_page(artist, album, track):
    return render_template("testsubject.html")
