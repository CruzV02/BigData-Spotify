#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

def preprocess(string):
    # Samuel dijo que queria una lista de listas...Si lo dije xd
    # cleaned_text = string.replace("<br/>", " ")
    cleaned_text = string.replace("<p>", "")
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

def getLyrics(author, song):
    page = getHTMLPage(author, song)
    soup = BeautifulSoup(page, "html.parser")

    title = soup.find("h1", class_="head-title")

    results = soup.find("div", class_="lyric-original")
    paragraps = results.find_all("p")

    result = []
    for para in paragraps:
        cleaned_text = preprocess(str(para))
        text_list = cleaned_text.split("<br/>")
        result.append(text_list)

    return result
