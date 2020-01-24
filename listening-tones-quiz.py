#!/usr/bin/python3

import json
import random
import sys
import argparse
import os
import numpy as np
import unicodedata
import random
from src.pinyinutil import *
import time
import requests
from bs4 import BeautifulSoup as bs

print("This quiz pulls data from https://www.hsk.academy.",flush=True)

root_urls = [
    "https://dictionary.hantrainerpro.com/chinese-english/"
]

# generates a list of words
def generate_index():
    index = []
    root_url = random.choice(root_urls)
    print("Index page ", root_url, flush=True)
    r = requests.get(root_url)
    if (r.status_code != 200):
        return []
    print("Loaded. Parsing...", flush=True)
        
    soup = bs(r.content, 'html.parser')
    print("Parsed", flush=True)
    rows = soup.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) != 4:
            continue
        pinyin_col = cols[1]
        
        # get link in td.
        a = pinyin_col.find_all("a")
        if len(a) == 1:
            a = a[0]
        else:
            continue
        
        # get pinyin text.
        pinyin_text = numeric_pinyin(a.get_text())
        print(pinyin_text)
        index.append({
            "pinyin": pinyin_text,
            "audio": "https://www.hantrainerpro.de/resources/pronunciations/" + pinyin_text + ".mp3",
            "filename": "data/" + pinyin_text + ".mp3"
        })
    return index
    
index = generate_index()

if len(index) == 0:
    print("Could not generate word index")
    sys.exit(1)

def download_word(word):
    if not os.path.exists("data/"):
        os.mkdir("data/")
    if os.path.exists(word["filename"]):
        print("Removing existing " + word["filename"])
        os.remove(word["filename"])
    if os.system("wget -O " + word["filename"] + " " + word["audio"] ):
        return False
    return os.path.exists(word["filename"])

def generate_word():
    return random.choice(index)
    
def play_word(word):
    os.system("mpg123 " + word["filename"] + " > /dev/null 2>&1")
    
while True:
    word = generate_word()
    if word is not None:
        if not download_word(word):
            print("Failed to download word " + word["audio"])
            continue
        while True:
            os.system("clear")
            print("Playing audio...")
            play_word(word)
            s = input("Pinyin > ")
            if s == "":
                continue
            if convert_pinyin(s) == convert_pinyin(word["pinyin"]):
                print("Correct!")
                input("Press any key to continue.")
                break
            else:
                print("Incorrect. The word was " + pretty_pinyin(word["pinyin"]))
                input("Press any key to acknowledge.")
                break
    else:
        print("Error generating word.")
        sys.exit(1)
