###################################
#  Program to simulate unigram model.
#
#  Author: Jorie Fernandez
#  Assignment 1
# 14 January 2018
###################################

TRAIN_FILE = 'doyle-27.txt'
TEST_FILE = 'doyle-case-27.txt'
UNIGRAM_PROB = 'unigram_probs.txt'
UNIGRAM_TEST = 'unigram_eval.txt'

from nltk.tokenize import regexp_tokenize
import re

#Read input file
def readFile(fileName):
    with open(fileName, 'r') as tf:
        text = tf.read()

    return text

#Unigram model implementation
def unigramModel(sentences):
    #tokenize individual words
    tk = regexp_tokenize(sentences, r'\S+')

    #sentence dictionary
    sentenceDict = {}

    #iterate through the list of words and update
    # the dictionary with the word and count
    for val, key in enumerate(tk):
        newKey = key.lower()
        #Check if key exists in the dictionary
        # If existing, upate count
        # If not, insert into the dictionary
        if newKey in sentenceDict:
            sentenceDict[newKey] += 1
        else:
            sentenceDict.update({newKey: 1})

    # return probability dictionary
    return (writeProbability(sentenceDict, len(tk)))

# Method to compute and write probabilities to the file
def writeProbability(wordDict, total):
    #probability dictionary
    probDict = {}

    #open file for writing and write probabilities
    with open(UNIGRAM_PROB, 'w') as wf:
        #iterate through the list of words and compute
        #probability of each word
        for key, val in wordDict.items():
            prob = (computeProbability(val, total))
            #insert probability into dictionary
            probDict.update({key: prob})
            #write into the file
            wf.write("P({}) = {}\n" .format(key, prob))
    #return probability dictionary
    return probDict

#Compute probability given the word count and total number of words
def computeProbability(wordCount, totalCount):
    return wordCount/totalCount

if __name__ == '__main__':
    #get sentences in the file
    sentences = readFile(TRAIN_FILE)
    # get probabilities of each word
    prob = unigramModel(sentences)

    #Counter for the first non-empty lines/sentences
    ctr = 0
    #open test file and unigram probability result
    with open(TEST_FILE, 'r') as tf, open(UNIGRAM_TEST, 'w') as wf:
        #iterate through the test file and compute the joint probability
        #and perplexity
        for index, line in enumerate(tf):
            sentprob = 1
            if ctr < 100:
                if line.strip():
                    ctr += 1
                    curStr = re.split(r'\s+', line.strip())
                    for word in curStr:
                        sentprob *= prob.get(word.lower(), 0)

                    wf.write("Line {}: Probability = {}\n" .format(ctr, sentprob))
                    if sentprob > 0:
                        perplexity = 1 / (pow(sentprob, 1.0 / (len(curStr))))
                        wf.write("\t   : Perplexity = {}\n" .format(perplexity))
                    else:

                        wf.write("\t   : Cannot compute perplexity due to zero probability.\n")

