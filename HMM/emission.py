###################################
#  Program to generate emission
#   probability.
#
#  Author: Jorie Fernandez
#  Assignment 2
#  4 February 2018
###################################

from nltk.tokenize import regexp_tokenize
import re
import pandas as pd

TRAIN = 'Klingon_Train.txt'
EMISSION = 'emission.csv'
SMOOTH_FACTOR = 0.1


# word and tag dictionary
wordtagDict = {}
#tag dictionary
tagDict = {}

# Count word and tag pair
def count_word_tag(sentence):
    # create the word and tag pair
    for sent in sentence:
        current_word =  (re.split(r'\/', sent))
        current_pair = (current_word[0], current_word[1])
        #update count
        if current_pair in wordtagDict:
            wordtagDict[current_pair] += 1
        else:
            wordtagDict.update({current_pair: 1})

        count_tag(current_word[1])

# count number of tags
def count_tag(tag):

    if tag in tagDict:
        tagDict[tag] += 1
    else:
        tagDict.update({tag: 1})

# Create emission probabilities
def create_emission():
    # Append unknown words
    words = list(set([item[0] for item in wordtagDict]))
    words.append('legh')
    words.append('yaS')
    words.sort()

    # create array for probabilities
    prob = create_array(words, tagDict)

    #compute probability
    for i in range(len(prob)):
        if(i > 0):
            for j in range(len(prob[i])):
                cur_word = prob[i][0]
                if(j > 0):
                    cur_tag = prob[0][j]
                    count_bi = wordtagDict.get((cur_word, cur_tag), 0)
                    count_tag = tagDict.get(cur_tag, 0)

                    prob[i][j] = compute_emission(count_bi, count_tag, len(tagDict))

    # Write probabilities to the csv file
    df = pd.DataFrame(prob)
    df.to_csv(EMISSION, header = None)

# create 2d array
def create_array(words, tag):
    # create 2d array
    row = len(words) + 1
    prob = [[SMOOTH_FACTOR] * (len(tag)+1) for i in range(row)]
    prob[0][0] = None
    row = 1
    for word in words:
        prob[row][0] = word
        row += 1

    col = 1
    for t in reversed(list(tag)):
        prob[0][col] = t
        col += 1

    return prob

# COmpute probability of word-tag pair
def compute_emission(bi_count, tag_count, total_tag):
    return ((bi_count + SMOOTH_FACTOR)/(tag_count + (SMOOTH_FACTOR* total_tag)))


if __name__ == '__main__':
    # Open training file and tokenize
    with open(TRAIN, 'r')as rf:
        for line in rf:
            word_tag = regexp_tokenize(line, r'\S+')
            count_word_tag(word_tag)
    # create emission probabilities
    create_emission()
