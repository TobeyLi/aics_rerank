import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ORIGINAL_DATA_DIR = "../data/original"
PROCESSED_DATA_DIR = "../data/processed"


def processJsonVocab(filePath, outputFilePath):
    if os.path.exists(outputVocabFilePath):
        logging.info("vocab file already exist,just use it:" + outputVocabFilePath)
        return

    with open(filePath, 'r') as fp:
        data = json.load(fp)
        id2word = data["id2word"]
    with open(outputFilePath, 'w') as fout:
        for index, val in id2word.items():
            fout.write(index + ":" + val.strip() + "\n")


def loadVocab(filePath):
    try:
        with open(filePath, 'r') as fp:
            data = json.load(fp)
            id2word = data["id2word"]
    except FileNotFoundError as e:
        logging.error(e)
    return id2word


def ids2Sentence(ids, id2word):
    sentence = []
    for id in ids:
        sentence.append(id2word[str(id)])
    return "".join(sentence)


def processJsonFile(inputFilePath, outputFilePath, id2word):
    if os.path.exists(outputFilePath):
        return
    logging.info("starting process "+outputFilePath.split("/")[-1].split(".")[0]+" file...")
    with open(inputFilePath, 'r') as fp:
        data = json.load(fp)
        with open(outputFilePath, 'w') as fout:
            for line in data:
                question = line["question"]
                utterance = line["utterance"]
                label = line["label"]
                query = ids2Sentence(question, id2word)
                answer = ids2Sentence(utterance, id2word)
                fout.write(query + "\t" + answer + "\t" + str(label[0]) + "\n")


if __name__ == '__main__':
    vocabFilePath = "../data/original/iqa.vocab.json"
    outputVocabFilePath = "../data/processed/vocab.txt"
    processJsonVocab(vocabFilePath, outputVocabFilePath)

    id2word = loadVocab(vocabFilePath)

    # process train、test、valid data
    processJsonFile(os.path.join(ORIGINAL_DATA_DIR, "iqa.train.json"),
                    os.path.join(PROCESSED_DATA_DIR, "train.txt"), id2word)

    processJsonFile(os.path.join(ORIGINAL_DATA_DIR, "iqa.test.json"),
                    os.path.join(PROCESSED_DATA_DIR, "test.txt"), id2word)

    processJsonFile(os.path.join(ORIGINAL_DATA_DIR, "iqa.valid.json"),
                    os.path.join(PROCESSED_DATA_DIR, "valid.txt"), id2word)
