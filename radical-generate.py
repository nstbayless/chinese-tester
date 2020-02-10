# scrapes a particular online list and generates a list of radicals.

src = "https://webcache.googleusercontent.com/search?q=cache:x2KP9IqXKPEJ:https://www.yellowbridge.com/chinese/radicals.php+&cd=12&hl=en&ct=clnk&gl=ca"

import requests
from bs4 import BeautifulSoup as bs
import sys
import os
import json
import src.pinyinutil as pinyinutil

print("getting webpage...", flush=True)
r = requests.get(src)
if (r.status_code != 200):
    print("Failed to load webpage.")
    sys.exit(1)
        
lists = [[] for i in range(32)]
soup = bs(r.content, 'html.parser')
print("Parsed", flush=True)
table = soup.find_all("table", {"class": "grid alignCenter sortable"})[0]
for tr in table.find_all("tr"):
    td = tr.find_all("td")
    if len(td) == 7:
        pinyin = td[4].contents[0]
        pinyin = pinyinutil.principal_vowel(pinyin)
        char = td[1].find("a").contents[0]
        meaning = td[5].contents[0]
        strokes = int("".join(td[6].contents))
        print(char, pinyin, meaning, strokes)
        word = {
            "character": [char],
            "pinyin": pinyin,
            "meaning": [meaning],
            "type": "radical"
        }
        lists[strokes].append(word)

i = 0
for l in lists:
    if len(l) > 0:
        with open("radicals/stroke-" + str(i) + ".json", "w") as f:
            json.dump(l, f)
    i += 1
