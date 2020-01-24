# Mandarin vocabulary tester

`python3 chinese-tester.py -cp path/to/vocab.json`

Helps you learn Chinese characters (汉字), Pinyin, and their associated English meanings. Just plug in a .json file with the dictionary of terms you're learning (or use any of the presets included in the repo) and select which quiz methods you prefer, and you're good to go!

## Recommended method for learning new vocab

1. First preview the vocab with the `-msc` (meaning-select-character *multiple choice*) command line flag,
2. Then learn the pinyin with `-pm` (pinyin-to-meaning),
3. Prove you know the characters and pinyin both with `-cp` (character-to-pinyin)

Skip directly to step 3 if you have some experience with the vocabulary already; return to step 1 or 2 if step 3 is too difficult.

Try to get at least 80% on step 1, 70% on step 2, then **aim for 100% on step 3**. The goal is to be able to associate characters, pinyin, and meaning. Doing well on step three ensures a character-pinyin association, which implies an underlying character-meaning-pinyin association. Step 1 and step 2 exist only to help prepare for step 3, so it is not important to get a perfect score.

To best retain your knowledge, use [spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition): revisit step 3 one day, one week, and one month later.

**Note:** this method is *not* sufficient for learning how to write the characters, only to read them. However, it *is* helpful for reading comprehension, listening comprehension, and verbal competence due to the reliance on pinyin.

## Learn the readicals

`python3 chinese-tester.py -cp radicals/stroke-2.json`

To improve your ability to learn new characters, you should study the meanings of the most common radicals. It's most important to associate radical-meaning.

## Sample Output

```
Type q or quit at any time to end.
Please type the pinyin for the following character:
十
P > shi2
shí
Correct!
FYI: 十 (shí) means "ten," or "10."

Please type the pinyin for the following character:
四
P > si4
sì
Correct!
FYI: 四 (sì) means "four," or "4."

Please type the meaning for the following pinyin:
yī
M > 1
Correct!
FYI: 一 (yī) means "one," or "1."

Please type the pinyin for the following character:
二
P > e4r
èr
Correct!
FYI: 二 (èr) means "two," or "2."

Please type the pinyin for a Mandarin word meaning the following:
eight
P > ba1
bā
Correct!
FYI: 八 (bā) means "eight," or "8."

Please type the pinyin for a Mandarin word meaning the following:
7
P > qi1
qī
Correct!
FYI: 七 (qī) means "seven," or "7."

Please type the meaning for the following character:
六
M > 6
Correct!
FYI: 六 (liù) means "six," or "6."

Please type the pinyin for the following character:
五
P > wu3
wǔ
Correct!
FYI: 五 (wǔ) means "five," or "5."

Which of the following characters means "3"?

  1. 十
  2. 八
  3. 一
  4. 三
  5. 五

(Please enter a number)
# > 4
Correct!
FYI: 三 (sān) means "three," or "3."

Please type the meaning for the following pinyin:
jiǔ
M > 9
Correct!
FYI: 九 (jiǔ) means "nine," or "9."

You're done! Score was 10/10
(That's 100.0%)
```
