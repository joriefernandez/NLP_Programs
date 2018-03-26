###################################
#  Program to simulate bigram language
#   model.
#
#  Author: Jorie Fernandez
#  Assignment 1
# 14 January 2018
###################################

from nltk.tokenize import regexp_tokenize
import random
import re

TRAIN_FILE = 'doyle-27.txt'
BIGRAM_PROB = 'bigram_probs.txt'
TEST_FILE = 'doyle-case-27.txt'
BIGRAM_TEST = 'bigram_eval.txt'

# list of words
wordDict = {}

# Read input file and return list of words
def readFile(fileName):
    with open(fileName, 'r') as rf:
        texts = rf.read()

    return regexp_tokenize(texts, r'\S+')

# Bigram model implementation
def bigram(sentences):

    # Set counts for each words
    setWordCount(sentences)
    # List of bigram words
    bigramDict = {}
    # Iterate through the list of words and create
    # bigrams to be inserted into bigram dictionary
    for index, val in enumerate(sentences):
        if(index > 0):
            current_bigram = (sentences[index-1].lower(), sentences[index].lower())

            if current_bigram in bigramDict:
                bigramDict[current_bigram] += 1
            else:
                bigramDict.update({current_bigram: 1})

    # return bigram dictionary
    return bigramDict

# Create a probability dictionary
def storeProbability(bigramDict):
    probDict = {}
    for key, val in bigramDict.items():
        prob = computeProb(val, getWordCount(key[0]))
        probDict.update({key: prob})

    return probDict

# Create a word dictionary with its corresponding frequency
def setWordCount(wordList):
    for val, key in enumerate(wordList):
        newKey = key.lower()
        if newKey in wordDict:
            wordDict[newKey] += 1
        else:
            wordDict.update({newKey: 1})

# Retrieve frequecy of a word
def getWordCount(word):
    return wordDict.get(word, 0)

# Write probabilities to the file
def writeProbabilityBigram(bigramDict):
    with open(BIGRAM_PROB, 'w') as bf:
        for ctr in range(0,100):
            randomWord =  random.choice(list(bigramDict))
            bf.write("P({}|{}) = {}\n" .format(randomWord[1], randomWord[0],
                                            (prob.get(randomWord, 0))))
#Compute probability of given bigram
def computeProb(pairCount, prevWordCount):
    return pairCount/prevWordCount

if __name__ == '__main__':
    # read input file
    sentences = readFile(TRAIN_FILE)
    # get bigram dictionary
    bigramDict = bigram(sentences)
    # get bigram probabilities
    prob = storeProbability(bigramDict)
    # write probabilities to the file
    writeProbabilityBigram(prob)

    # Counter for lines
    ctr = 0

    # Evaluate test file
    with open(TEST_FILE, 'r') as tf, open(BIGRAM_TEST, 'w') as wf:
        for index, line in enumerate(tf):
            sentprob = 1
            if ctr < 100:
                if line.strip():
                    ctr += 1
                    curStr = re.split(r'\s+', line.strip())


                    for index, val in enumerate(curStr):

                        if(index > 0):
                            curKey = (curStr[index-1].lower(), curStr[index].lower())


                            sentprob *= prob.get(curKey, 0)

                    wf.write("Line {}: Probability = {}\n" .format(ctr, sentprob))
                    if sentprob > 0:
                        perplexity = 1 / (pow(sentprob, 1.0 / (len(curStr))))
                        wf.write("\t\t: Perplexity = {}\n" .format(perplexity))
                    else:

                        wf.write("\t\t: Cannot compute perplexity due to zero probability.\n")


