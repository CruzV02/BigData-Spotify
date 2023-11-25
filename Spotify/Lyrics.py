#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

def preprocess(string):
    cleaned_text = string.replace("<br/>", " ")
    cleaned_text = cleaned_text.replace("<p>", "")
    cleaned_text = cleaned_text.replace("</p>", "")

    return cleaned_text

def cleanAuthor(string):
    cleaned_text = string.replace("(", "")
    cleaned_text = cleaned_text.replace(")", "")
    cleaned_text = cleaned_text.lower()

    return cleaned_text

def getHTMLPage(author, song):
    cleanedAuthor = cleanAuthor(author)
    cleanedSong = song.lower().replace(" ", "-")
    URL = f"https://www.letras.com/{cleanedAuthor}/{cleanedSong}/"

    page = requests.get(URL)
    print("URL:", URL)  # Imprime la URL

    if (not page.ok) :
        raise Exception("Author not found.")

    return page.content

def getLyrics(author, song, html=False):
    page = getHTMLPage(author, song)
    soup = BeautifulSoup(page, "html.parser")

    title = soup.find("h1", class_="head-title")
    # Si hubo una redirección
    if (not page.ok):
        raise Exception("Couldn't find a song with that name.")

    results = soup.find("div", class_="lyric-original")
    paragraps = results.find_all("p")

    if(html):
        return paragraps

    result = []
    for para in paragraps:
        cleaned_text = preprocess(str(para))
        result.append(cleaned_text)

    return result
