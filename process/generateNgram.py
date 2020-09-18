import jieba
import pandas as pd
from collections import Counter

# 导入自定义
jieba.load_userdict("../resource/tokenizer/userDict.txt")


def loadData(inputFilePath):
    res = []
    with open(inputFilePath, 'r') as fin:
        lines = fin.readlines()
    for line in lines:
        line = line.split("\t")
        if line[0] not in res:
            res.append(line[0])
        if line[1] not in res:
            res.append(line[1])
    return res


def dropDuplicates(data):
    sentenceFrame = pd.DataFrame({"sentence": data})
    return sentenceFrame.drop_duplicates().sentence.values


def generateNGrams(s, gram):
    tokens = [token for token in s if token != ""]

    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(gram)])
    return [" ".join(ngram) for ngram in ngrams]

def getNGrams(datas,gram):
    res=[]
    for data in datas:
        jiebaRes=list(jieba.cut(data))
        res.extend(generateNGrams(jiebaRes,gram))
    return res

def writeNGramTofile(gramDict:dict,outputFilePath):
    with open(outputFilePath,'w') as fout:
        for key,value in gramDict.items():
            fout.write(key+":"+str(value)+"\n")


if __name__ == '__main__':
    trainData = "../data/processed/train.txt"
    testData = "../data/processed/test.txt"
    validData = "../data/processed/valid.txt"

    allData = []
    allData.extend(loadData(trainData))
    allData.extend(loadData(testData))
    allData.extend(loadData(validData))
    #
    nonDuplicatesData = dropDuplicates(allData)

    # generate gram
    unigram=getNGrams(nonDuplicatesData,gram=1)
    bigram=getNGrams(nonDuplicatesData,gram=2)

    # counter
    unigramCounter=Counter(unigram)
    bigramCounter=Counter(bigram)

    # write to file
    unigramOutputFilePath = "../resource/ngram/unigram.txt"
    bigramOutputFilePath="../resource/ngram/bigram.txt"

    writeNGramTofile(unigramCounter,unigramOutputFilePath)
    writeNGramTofile(bigramCounter,bigramOutputFilePath)