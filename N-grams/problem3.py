###################################
#  Program to simulate bigram language
#   model with smoothing k = 0.10.
#
#  Author: Jorie Fernandez
#  Assignment 1
# 14 January 2018
###################################

from nltk.tokenize import regexp_tokenize
import re


TRAIN_FILE = 'doyle-27.txt'
BIGRAM_PROB = 'bigram_probs.txt'
TEST_FILE = 'doyle-case-27.txt'
SMOOTH_TEST = 'smoothed_eval.txt'
SMOOTH_PROB = 'smooth_probs.txt'
K = 0.10

#Word dictionary
wordDict = {}
# Read input file and return the words
def readFile(fileName):
    with open(fileName, 'r') as rf:
        texts = rf.read()

    return regexp_tokenize(texts, r'\S+')

# Bigram with smoothing
def bigram(sentences):

    # set word count
    setWordCount(sentences)
    # bigram dictionary
    bigramDict = {}
    #Iterate through the list of sentences and
    # create bigrams to be stored in the
    # dictionary with its count
    for index, val in enumerate(sentences):
        if(index > 0):
            current_bigram = (sentences[index-1].lower(), sentences[index].lower())
            if current_bigram in bigramDict:
                bigramDict[current_bigram] += 1
            else:
                bigramDict.update({current_bigram: 1})

    # return bigram dictionary
    return bigramDict

# Compute and Create list of bigram probability
def storeProbability(bigramDict):
    probDict = {}
    for key, val in bigramDict.items():
        prob = computeProb(val, getWordCount(key[0]))

        probDict.update({key: prob})

    return probDict

# Set word count
def setWordCount(wordList):
    for val, key in enumerate(wordList):
        newKey = key.lower()
        if newKey in wordDict:
            wordDict[newKey] += 1
        else:
            wordDict.update({newKey: 1})

# Get frequency of a word. K value is
# assigned to non-existent key
def getWordCount(word):
    return wordDict.get(word, K)

#Write probability of the bigram
def writeProbabilityBigram(probDict):
    with open(SMOOTH_PROB, 'w') as bf, open(BIGRAM_PROB, 'r')as rf:

        for line in rf:

            randomWord = re.split(r'\|', re.search(r'(?<=P\()\w+\|\w+', line).group(0))
            curKey = (randomWord[1], randomWord[0])
            unknownProb = computeProb(0, getWordCount(randomWord[0]))
            bf.write("P({}|{}) = {}\n" .format(randomWord[0], randomWord[1],
                                           (probDict.get(curKey, unknownProb))))

# Compute probability of the bigram
def computeProb(pairCount, prevWordCount):
    return ((pairCount + K) / (prevWordCount + (len(wordDict) * K)))

if __name__ == '__main__':
    #read input file
    sentences = readFile(TRAIN_FILE)
    # get bigram dictionary
    bigramDict = bigram(sentences)
    # get bigram probabilities
    prob = storeProbability(bigramDict)
    # Write probabilities to the file
    writeProbabilityBigram(prob)

    #Evaluate test file
    ctr = 0
    with open(TEST_FILE, 'r') as tf, open(SMOOTH_TEST, 'w') as wf:
        for index, line in enumerate(tf):
            sentprob = 1
            if ctr < 100:
                if line.strip():
                    ctr += 1
                    curStr = re.split(r'\s+', line.strip())
                    curKey = ()
                    for index, val in enumerate(curStr):
                        if(index > 0):
                            curKey = (curStr[index-1].lower(), curStr[index].lower())
                            unknownProb = computeProb(0, getWordCount(curStr[index-1].lower()))

                            sentprob *= prob.get(curKey, unknownProb )


                    wf.write("Line {}: Probability = {}\n" .format(ctr, sentprob))

                    if sentprob > 0:
                        perplexity = 1 / (pow(sentprob, 1.0 / (len(curStr))))
                        wf.write("\t  : Perplexity = {}\n" .format(perplexity))
                    else:

                        wf.write("\t  : Cannot compute perplexity due to zero probability.\n")

