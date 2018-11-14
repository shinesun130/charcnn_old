#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import json

if len(sys.argv) < 5:
  print >> sys.stderr, "Usage: %s hanzi2PinyinPath labelVal rawTextPath outPinyinTextPath" % sys.argv[0]
  sys.exit(-1)
hanzi2PinyinPath = sys.argv[1]
labelVal = sys.argv[2]
rawTextPath = sys.argv[3]
outPinyinTextPath = sys.argv[4]

## check label value
if labelVal != "-1" and labelVal != "1":
  raise IOError, "Illegal label value %s, it should be -1 or 1" % labelVal
stars = 5
if labelVal == "1":
  stars = 5
elif labelVal == "-1":
  stars = 1

## Construct the hanzi to pinyin dict
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
allCharMapDict = {}
## chinese punctuation map to english punctuation
chnPunctuationStr = "，；。！？：‘’“”、｜－@＃¥％…＊～｀＋－—＝《》（）［］【】｛｝"
decChnPunctuationStr = chnPunctuationStr.decode("utf-8", "ignore")
engPunctuationStr = ",;.!?:''\"\"\|_@#$%^*~`+--=<>()[][]{}"
if len(decChnPunctuationStr) != len(engPunctuationStr):
  raise IOError, "chinese punctuation length is not equal to corresponding english punctuation length"
for i in range(0, len(decChnPunctuationStr)):
  allCharMapDict[decChnPunctuationStr[i]] = engPunctuationStr[i]
## add the alphabet to dict
alphabet = " \tABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-,;.!?:'\"/\\|_@#$%^&*~`+-=<>()[]{}"
for i in range(0, len(alphabet)):
  allCharMapDict[alphabet[i]] = alphabet[i]
## add the hanzi to pinyin dict
hanzi2PinyinDict = {}
hanzi2PinyinInHler = open(hanzi2PinyinPath, "r")
for line in hanzi2PinyinInHler:
  line = line.strip()
  decLine = line.decode("utf-8", "ignore")
  parts = decLine.split("\t")
  if len(parts) != 2:
    #raise IOError, "Illegal hanzi to pinyin line"
    continue
  hanzi2PinyinDict[parts[0]] = parts[1]
hanzi2PinyinInHler.close()

## convert the hanzi weibo to pinyin
os.system("rm -fr %s" % outPinyinTextPath)
outPinyinTextHler = open(outPinyinTextPath, "w")
rawTextInHler = open(rawTextPath, "r")
for line in rawTextInHler:
  outMsg = ""
  line = line.strip()
  decLine = line.decode("utf-8", "ignore")
  decLine = decLine.lower()
  for i in range(0, len(decLine)):
    singleChar = decLine[i]
    if singleChar in hanzi2PinyinDict:
      chnCharPinyin = hanzi2PinyinDict[singleChar]
      outMsg += (" " + chnCharPinyin)
    elif singleChar in allCharMapDict:
      newChar = allCharMapDict[singleChar]
      outMsg += newChar
  outMsg = outMsg.strip()
  outJsonObj = {}
  outJsonObj['stars'] = stars
  outJsonObj['text'] = outMsg
  jsonMsg = json.dumps(outJsonObj)
  #jsonMsg = "{\"stars\":%s, \"text\":%s}\n" % (stars, outMsg)
  outPinyinTextHler.write(jsonMsg + "\n")
      
rawTextInHler.close()
