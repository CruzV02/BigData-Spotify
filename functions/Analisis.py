from textblob import TextBlob
import pandas as pd

from functions.Lyrics import getLyrics
from functions.Promedio import getTrackData
from functions.Spotify import spotify


def album_analisis(tracks=[], album_id="0", artist_id="0", ):
    df=pd.DataFrame()
    for track in tracks:
        insert = pd.DataFrame(
            [
                {
                    "track_id": track["id"],
                    "track_name": track["name"],
                    "album_id": album_id,
                    "artist_id": artist_id,
                    "lyrics": getLyrics(track["artists"][0]["name"], track["name"]),
                    "duration": track["duration_ms"],
                }
            ]
        )

        df = pd.concat([df, insert], ignore_index=True)
        df[["polarity", "subjectivity"]] = df.lyrics.astype(str).apply(
            lambda Text: pd.Series(TextBlob(Text).sentiment)
        )

        df[
            [
                "danceability",
                "energy",
                "speechiness",
                "acousticness",
            ]
        ] = getTrackData(track["id"])

    return df


def track_analisis(track_id="", album_id="0", artist_id="0", df=pd.DataFrame()):
    track = spotify.track(track_id)

    insert = pd.DataFrame(
        [
            {
                "track_id": track_id,
                "track_name": track["name"],
                "album_id": album_id,
                "artist_id": artist_id,
                "lyrics": getLyrics(track["artists"][0]["name"], track["name"]),
                "duration": track["duration_ms"],
            }
        ]
    )

    df = pd.concat([df, insert], ignore_index=True)
    df[["polarity", "subjectivity"]] = df.lyrics.astype(str).apply(
        lambda Text: pd.Series(TextBlob(Text).sentiment)
    )

    df[
        [
            "danceability",
            "energy",
            "speechiness",
            "acousticness",
        ]
    ] = getTrackData(track_id)

    return df
