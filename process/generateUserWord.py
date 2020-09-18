# 按照不同的分词器结果，生成专用词表
import jieba


def processVocab(vocabFilePath):
    with open(vocabFilePath, 'r') as fp:
        lines = fp.readlines()
    return list(map(lambda line: line.strip().split(":")[1], lines))


def getDifferenceBetweenTwoTokenizer(originalWords):
    """
    统一两个分词器的分词结果，为非标准分词器生成词典
    :param originalWords: 标准分词器的分词结果
    :return:
    """
    difference = []
    for word in words:
        jiebaRes = list(jieba.cut(word))
        if len(jiebaRes) > 1:
            difference.append(word)
    return difference


def generateUserDict(outputUserDictFilePath,differenceWords):
    with open(outputUserDictFilePath,'w') as fout:
        for word in differenceWords:
            fout.write(word.strip()+"\n")


if __name__ == '__main__':
    vocabPath = "../data/processed/vocab.txt"
    words = processVocab(vocabPath)

    differenceWords = getDifferenceBetweenTwoTokenizer(words)

    # generate difference words
    outputDifferenceFilePath="../data/processed/userDict.txt"
    generateUserDict(outputDifferenceFilePath,differenceWords)
