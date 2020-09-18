import collections
import jieba
import math
import sys
sys.path.append("..")
import os
import numpy as np

jieba.load_userdict("../../../resource/tokenizer/userDict.txt")


class NGram:
    def __init__(self, unigram, bigram, *args, **kwargs):
        self.unigram = unigram
        self.bigram = bigram

    def getProbabity(self, sentence):
        if len(sentence) < 0:
            return 0
        senteceTokernization = list(jieba.cut(sentence))
        p = (self.unigram.get(senteceTokernization[0]) + 0.01) / (len(self.unigram) + 0.01)
        for i in range(1, len(senteceTokernization)):
            p *= (self.bigram.get(senteceTokernization[i - 1] + " " + senteceTokernization[i]) + 0.01) / (
                    len(self.bigram) + 0.01)
        return math.log(p)


def loadNgram(nGramFilePath):
    nGramDict = collections.defaultdict()
    with open(nGramFilePath, 'r') as fin:
        lines = fin.readlines()
    for line in lines:
        line = line.split(":")
        nGramDict[line[0]] = int(line[1])
    return nGramDict

if __name__ == '__main__':
    unigramPath="../../../resource/ngram/unigram.txt"
    bigramPath="../../../resource/ngram/bigram.txt"

    unigram=loadNgram(unigramPath)
    bigram=loadNgram(bigramPath)

    nGram=NGram(unigram,bigram)

    sentence="什么是私人健康保险"
    print(nGram.getProbabity(sentence))
