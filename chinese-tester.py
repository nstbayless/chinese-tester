import json
import random
import sys

def convert_pinyin(pinyin):
	# converts pinyin to standardized form
	pinyin = pinyin.replace("0","")
	
	return pinyin;

def meaning_to_pinyin(v,vocab):
	print("Please type the pinyin for Mandarin word meaning the following:")
	my_meaning = random.choice(v["meaning"])
	print(my_meaning)
	in_pinyin = raw_input("P > ")
	if convert_pinyin(in_pinyin) == v["pinyin"]:
		print "Correct!"
		return 1
	for v2 in vocab:
		if v2["pinyin"] == in_pinyin:
			if my_meaning in v2["meaning"]:
				print ("Correct, although I had intended the pinyin " + v["pinyin"] + ".")
	print "Incorrect. The only pinyin matching that meaning in the given vocabulary file is " + v["meaning"][0]
	return 0

def pinyin_to_meaning(v,vocab):
	print("Please type the meaning for the following pinyin:")
	print(v["pinyin"])
	in_meaning = raw_input("M > ")
	if in_meaning.lower() in map(lambda x: x.lower(), v["meaning"]):
		print "Correct!"
		return 1
	if len(v["meaning"]) == 1:
		print "Incorrect. The correct meaning is " + v["meaning"][0]
	else:
		print "Incorrect. The correct meanings are " + ", ".join(v["meaning"])
	return 0
	
def main (vocab,methods):
	maxscore = 0
	score = 0
	random.shuffle(vocab)
	for v in vocab:
		maxscore += 1
		fn = random.choice(methods);
		t_score = fn(v,vocab)
		score += t_score
		if t_score < 1:
			raw_input("Press Enter to acknowledge. ")
	print("You're done! Score was " + str(score) + "/" + str(maxscore))
	print("(That's " + '{0:.1f}'.format(float(score)/maxscore * 100.0) + "%)")
	
with open("vocab.json", "r+") as f:
	vocab = json.loads(f.read())
	main(vocab, [pinyin_to_meaning, meaning_to_pinyin]) #,pinyin_to_meaning,character_to_pinyin,meaning_select_character,pinyin_select_character])