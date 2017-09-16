import json
import random
import sys
import argparse
import numpy as np

class QuitException(Exception):
  pass
  
class MissingDataException(Exception):
  pass

def check_quit(s):
  if s == "q" or s == "quit":
    raise QuitException

def convert_pinyin(pinyin):
  # converts pinyin to standardized form
  pinyin = pinyin.replace("0","")
  
  return pinyin;
  
def standard_meaning(m):
  m = m.lower()
  if (m.startswith("to ")):
    m = m[3:]
  return m

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
      ri = raw_input("# > ")
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
  print("Please type the pinyin for Mandarin word meaning the following:")
  my_meaning = random.choice(v["meaning"])
  print(my_meaning)
  in_pinyin = raw_input("P > ")
  check_quit(in_pinyin)
  if convert_pinyin(in_pinyin) == v["pinyin"]:
    print "Correct!"
    return 1
  for v2 in vocab:
    if v2["pinyin"] == in_pinyin:
      if my_meaning in v2["meaning"]:
        print ("Correct, although I had intended the pinyin " + v["pinyin"] + ".")
  print("Incorrect. A correct answer would have been " + v["pinyin"])
  return 0

def pinyin_to_meaning(v,vocab):
  print("Please type the meaning for the following pinyin:")
  print(v["pinyin"])
  in_meaning = raw_input("M > ")
  check_quit(in_meaning)
  if standard_meaning(in_meaning) in map(standard_meaning, v["meaning"]):
    print "Correct!"
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
  
  in_pinyin = raw_input("P > ")
  check_quit(in_pinyin)
  
  if convert_pinyin(in_pinyin) == v["pinyin"]:
    print "Correct!"
    return 1
  print("Incorrect. The pinyin for " + character + " is " + v["pinyin"] + ".")
  return 0
  
def character_to_meaning(v, vocab):
  if len(v["character"]) == 0:
    raise MissingDataException("no character")
  print("Please type the meaning for the following character:")
  character = random.choice(v["character"])
  print(character)
  
  in_meaning = raw_input("M > ")
  check_quit(in_meaning)
  
  if standard_meaning(in_meaning) in map(standard_meaning, v["meaning"]):
    print "Correct!"
    return 1
  if len(v["meaning"]) == 1:
    print("Incorrect. The meaning for " + character + " is " + v["meaning"][0])
  else:
    print("Incorrect. The meanings for " + character + " are " + ", ".join(v["meaning"]))
  return 0

def main (vocab,methods):
  maxscore = 0
  score = 0
  random.shuffle(vocab)
  print("Quiz begins now.")
  print("Type q or quit at any time to end.")
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
        success = True
        print ("FYI: " + "/".join(v["character"]) + " (" + v["pinyin"] + ") means \"" + ",\" or \"".join(v["meaning"]) + ".\"")
        if t_score < 1:
          raw_input("Press Enter to acknowledge. ")
        break
      if not success:
        print("Could not quiz you on one of the vocabulary items, as it\nlacked data... please select additional quizzing methods.")
        break
  except QuitException:
    pass
  print("You're done! Score was " + str(score) + "/" + str(maxscore))
  print("(That's " + '{0:.1f}'.format(float(score)/maxscore * 100.0) + "%)")
  
vocab = []
methods = [character_to_meaning,character_to_pinyin,pinyin_to_meaning,meaning_to_pinyin,meaning_select_character]

parser = argparse.ArgumentParser(description='Practice Chinese.')
parser.add_argument('file', type=argparse.FileType('r'), nargs='+')

args = parser.parse_args()

for f in args.file:
  #with open(fa, "r+") as f:
    vocab.extend(json.loads(f.read()))

if len(methods) <= 0:
  print("Need at least one quizzing method (try --text for all non-audio methods)")
  sys.exit(-1)
  
if len(vocab) <= 0:
  print("Need at least one vocab word")
  sys.exit(-2)

main(vocab, methods)
