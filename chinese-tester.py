#!/usr/bin/python3

import json
import random
import sys
import argparse
import os
import numpy as np
import unicodedata
from src import generate
from src.pinyinutil import *
import time

audio_enabled = True
try:
  from gtts import gTTS
  from playsound import playsound
except:
  audio_enabled = False

xpin_enabled = True
try:
  from xpinyin import Pinyin
  xpin = Pinyin()
except:
  xpin_enabled = False

def print_pinyin_help():
  pinyin = "xia3ojie3"
  if random.random() > 0.5:
    pinyin = "xia1nsheng"
  print("Write numbers after the principal vowel to indicate tone in pinyin.")
  print("For example: " + pinyin + " becomes " + pretty_pinyin(pinyin) + ".")

def xpinyin_unit():
  global xpin
  print("Please enter the pinyin for the following sound.")
  my_char = chr(0x4e00 + int(random.random()*0x4189))
  while True:
    play_audio(my_char)
    pinyin_expected = xpin.get_pinyin(my_char, '', show_tone_marks = True)
    in_pinyin = input("P > ")
    check_quit(in_pinyin)
    if in_pinyin == "p":
      continue
    print(pretty_pinyin(in_pinyin))

    if unicodedata.normalize('NFC', pinyin_expected) == unicodedata.normalize('NFC', pretty_pinyin(in_pinyin)):
      print("Correct!")
      return 1
    print("Incorrect. The correct answer was " + pinyin_expected + ": " + my_char)
    return 0

def xpinyin_test():
  if not xpin_enabled:
    print("xpinyin library needs to be installed.")
    return -1

  print("Testing arbitrary audio-to-pinyin comprehension.")
  print_pinyin_help()
  print("Quiz begins now.")
  score = 0
  maxscore = 0
  try:
    while True:
      tscore = xpinyin_unit()
      score += tscore
      if (tscore < 1):
        input("Press Enter to acknowledge. ")
      maxscore += 1
  except QuitException:
    pass
  print("You're done! Score was " + str(score) + "/" + str(maxscore))
  if maxscore > 0:
    print("(That's " + '{0:.1f}'.format(float(score)/maxscore * 100.0) + "%)")

class QuitException(Exception):
  pass

class MissingDataException(Exception):
  pass

def check_quit(s):
  if s == "q" or s == "quit":
    raise QuitException

def standard_meaning(m):
  m = m.lower()
  m = m.strip()
  if (m.startswith("to ")):
    m = m[3:]
  if (m.startswith("a ")):
    m = m[2:]
  if (m.endswith("...")):
    m = m[:-3]
  return m

def play_audio(character):
  gtts = gTTS(text=character, lang="zh")
  gtts.save("/tmp/tts.mp3")
  playsound("/tmp/tts.mp3")
  os.remove("/tmp/tts.mp3")

def audio_to_pinyin(v, vocab):
  if not audio_enabled:
    print("gTTS and playsound needed to perform audio-to-pinyin quizzing.")
    raise MissingDataException("missing library")
  if len(v["character"]) == 0:
    raise MissingDataException("no character")
  print("Please listen to the following audio.")

  while True:
    play_audio(random.choice(v["character"]))
    print('type "P" to play again.')
    in_pinyin = input("P > ")
    if in_pinyin == "p":
      continue
    check_quit(in_pinyin)
    print(pretty_pinyin(in_pinyin))


    if convert_pinyin(v["pinyin"]) == convert_pinyin(in_pinyin):
      print("Correct!")
      return 1
    print ("Incorrect.")
    return 0

def meaning_select_character(v,vocab):
  my_meaning = random.choice(v["meaning"])
  if len(v["character"]) == 0:
    raise MissingDataException("no character")
  # construct list of options:
  vlist = [v]
  for i in range(5):
    v2 = random.choice(vocab);
    if v2 not in vlist:
      vlist.append(v2)

  random.shuffle(vlist)

  print("Which of the following characters means \"" + my_meaning + "\"?")
  print("")
  for i,v2 in enumerate(vlist):
    print ("  " +str(i+1)+". " + random.choice(v2["character"]))

  print("")
  while True:
    print("(Please enter a number)")
    try:
      ri = input("# > ")
      check_quit(ri)
      n = int(ri)
      if n <= 0 or n > len(vlist):
        print ("Invalid choice.")
        continue
      if my_meaning in vlist[n-1]["meaning"]:
        print ("Correct!")
        return 1
      print ("Incorrect. The correct choice was " + "/".join(v["character"]) + ".")
      return 0
    except ValueError:
      continue


def meaning_to_pinyin(v,vocab):
  print("Please type the pinyin for a Mandarin word meaning the following:")
  my_meaning = random.choice(v["meaning"])
  print(my_meaning)
  in_pinyin = input("P > ")
  print(pretty_pinyin(in_pinyin))

  check_quit(in_pinyin)
  if convert_pinyin(in_pinyin) == convert_pinyin(v["pinyin"]):
    print("Correct!")
    return 1
  for v2 in vocab:
    if convert_pinyin(v2["pinyin"]) == convert_pinyin(in_pinyin):
      if standard_meaning(my_meaning) in map(standard_meaning, v2["meaning"]):
        print ("Correct, although I had intended the pinyin " + pretty_pinyin(v["pinyin"]) + ".")
        return 1
  print("Incorrect. A correct answer would have been " + pretty_pinyin(v["pinyin"]))
  return 0

def pinyin_to_meaning(v,vocab):

  print("Please type the meaning for the following pinyin:")
  print(pretty_pinyin(v["pinyin"]))
  in_meaning = input("M > ")
  check_quit(in_meaning)

  if standard_meaning(in_meaning) in map(standard_meaning, v["meaning"]) or \
      standard_meaning(in_meaning) in map(standard_meaning, v["meaning-accepted"]):
    print("Correct!")
    return 1
  if len(v["meaning"]) == 1:
    print("Incorrect. The correct meaning is " + v["meaning"][0])
  else:
    print("Incorrect. The correct meanings are " + ", ".join(v["meaning"]))
  return 0

def character_to_pinyin(v, vocab):
  if len(v["character"]) == 0:
    raise MissingDataException("no character")
  print("Please type the pinyin for the following character:")
  character = random.choice(v["character"])
  print(character)

  in_pinyin = input("P > ")
  check_quit(in_pinyin)
  print(pretty_pinyin(in_pinyin))

  if convert_pinyin(in_pinyin) == convert_pinyin(v["pinyin"]):
    print("Correct!")
    return 1
  print("Incorrect. The pinyin for " + character + " is " + pretty_pinyin(v["pinyin"]) + ".")
  return 0

def character_to_meaning(v, vocab):
  if len(v["character"]) == 0:
    raise MissingDataException("no character")
  print("Please type the meaning for the following character:")
  character = random.choice(v["character"])
  print(character)

  in_meaning = input("M > ")
  check_quit(in_meaning)

  if standard_meaning(in_meaning) in map(standard_meaning, v["meaning"]) \
    or standard_meaning(in_meaning) in map(standard_meaning, v["meaning-accepted"]):
    print("Correct!")
    return 1
  if len(v["meaning"]) == 1:
    print("Incorrect. The meaning for " + character + " is " + v["meaning"][0])
  else:
    print("Incorrect. The meanings for " + character + " are " + ", ".join(v["meaning"]))
  return 0

def quiz (vocab,methods, retest):
  random.shuffle(vocab)
  for v in vocab:
    sys.stdout.write(pretty_pinyin(v["pinyin"]))
    sys.stdout.flush()
    time.sleep(1)
    sys.stdout.write(" " +random.choice(v["character"]))
    sys.stdout.flush()
    time.sleep(1)
    sys.stdout.write(" " +random.choice(v["meaning"]))
    sys.stdout.flush()
    time.sleep(2)
    print("")
  

def quiz (vocab,methods, retest):
  maxscore = 0
  score = 0
  random.shuffle(vocab)
  print_pinyin_help()
  print("Type q or quit at any time to end.")
  print("Quiz begins now.")
  try:
    for v in vocab:
      random.shuffle(methods)
      success = False
      for fn in methods:
        t_score = -1
        try:
          t_score = fn(v,vocab)
        except MissingDataException:
          continue
        score += t_score
        maxscore += 1
        if t_score == 0 and retest:
          vocab.append(v)
        success = True
        print ("FYI: " + "/".join(v["character"]) + " (" + pretty_pinyin(v["pinyin"]) + ") means \"" + ",\" or \"".join(v["meaning"]) + ".\"\n")
        if t_score < 1:
          input("Press Enter to acknowledge. ")
        break
      if not success:
        #print("Could not quiz you on one of the vocabulary items, as it\nlacked data... please select additional quizzing methods.")
        continue
  except QuitException:
    pass
  print("You're done! Score was " + str(score) + "/" + str(maxscore))
  if maxscore > 0:
    print("(That's " + '{0:.1f}'.format(float(score)/maxscore * 100.0) + "%)")

vocab = []
methods = []

parser = argparse.ArgumentParser(description='Practice Chinese.')
parser.add_argument('file', type=argparse.FileType('r'), nargs='+', help="JSON file containing vocabulary dictionary")
parser.add_argument('--characters',action = 'store_true')
parser.add_argument('--all',action = 'store_true')
parser.add_argument('--text',action = 'store_true')
parser.add_argument('--pinyin',action = 'store_true')
parser.add_argument('--list',action = 'store_true')
parser.add_argument('-msc',action = 'store_true')
parser.add_argument('-mp',action = 'store_true')
parser.add_argument('-pm',action = 'store_true')
parser.add_argument('-cm',action = 'store_true')
parser.add_argument('-cp',action = 'store_true')
parser.add_argument('-ap',action = 'store_true')
parser.add_argument('-axp',action = 'store_true')
parser.add_argument('--retest-failure',action = 'store_true')
parser.add_argument('--generate-sentences',action = 'store_true')

args = parser.parse_args()

if args.all:
  methods.extend([character_to_meaning,character_to_pinyin,pinyin_to_meaning,meaning_to_pinyin,meaning_select_character])
  if audio_enabled:
    methods.extend([audio_to_pinyin])

if args.text:
  methods.extend([character_to_meaning,character_to_pinyin,pinyin_to_meaning,meaning_to_pinyin,meaning_select_character])

if args.characters:
  methods.extend([character_to_meaning,character_to_pinyin,meaning_select_character])

if args.pinyin:
  methods.extend([character_to_pinyin, pinyin_to_meaning, meaning_to_pinyin])

if args.msc:
  methods.append(meaning_select_character)

if args.mp:
  methods.append(meaning_to_pinyin)

if args.pm:
  methods.append(pinyin_to_meaning)

if args.cm:
  methods.append(character_to_meaning)

if args.cp:
  methods.append(character_to_pinyin)

if args.ap:
  methods.append(audio_to_pinyin)

if args.axp:
  xpinyin_test()
  sys.exit()

# remove duplicates
methods = list(set(methods))

for f in args.file:
  #with open(fa, "r+") as f:
  try:
    vocab.extend(json.loads(f.read()))
  except json.decoder.JSONDecodeError as e:
    print("\nError in file " + str(f.name))
    raise e;


for v in vocab:
  v.setdefault("character",[])
  v.setdefault("pinyin","")
  v.setdefault("meaning",[])
  v.setdefault("meaning-accepted",[])
  v.setdefault("type",[])
  v.setdefault("hint","")

if (args.generate_sentences):
    print(generate.sentence(vocab))
    sys.exit(0)

if len(methods) <= 0:
  print("Need at least one quizzing method (try --text for all non-audio methods)")
  sys.exit(-1)

if len(vocab) <= 0:
  print("Need at least one vocab word")
  sys.exit(-2)
  
if len(methods) <= 0:
  print("Need at least one quizzing method (try --text for all non-audio methods)")
  sys.exit(-1)
  
quiz(vocab, methods, args.retest_failure)
