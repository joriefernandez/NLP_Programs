###################################
#  Program to generate transition
#   probability.
#
#  Author: Jorie Fernandez
#  Assignment 2
#  4 February 2018
###################################


from nltk.tokenize import regexp_tokenize
import pandas as pd

TRAIN = 'Klingon_Train.txt'
TRANSITION = 'transition.csv'
SMOOTH_FACTOR = 0.1

# Tag pair count
tagseq = {}

# Tag count
tagcount = {}

# Count pair of tags
def count_tag_pair(tags):
    #create pair of tags and counts
    for index in range(len(tags)):

        count_tag(tags[index])
        # check if the pair already exists in the list. If not, add
        # to the list.
        if (index > 0):
            pair = (tags[index - 1], tags[index])
            if pair in tagseq:
                tagseq[pair] += 1
            else:
                tagseq.update({pair: 1})

# Count number of tags
def count_tag(tag):
    if tag not in tagcount:
        tagcount.update({tag: 1})
    else:
        tagcount[tag] += 1


# Compute transition probability for tag pair
def compute_transition(bi_count, tag_count, total_tag):
    return ((bi_count + SMOOTH_FACTOR)/(tag_count + (total_tag * SMOOTH_FACTOR)))

# Create transition probabilities of words
def create_transition():

    prob = create_array(tagcount)

    #compute probability
    for i in range(len(prob)):
        if(i > 0):
            for j in range(len(prob[i])):

                row_tag = prob[i][0]

                if(j > 0):
                    col_tag = prob[0][j]
                    count_bi = tagseq.get((row_tag, col_tag), 0)
                    count_tag = tagcount.get(row_tag, 0)

                    prob[i][j] = compute_transition(count_bi, count_tag, len(tagcount)-1)

    # write probabilities to the csv file
    df = pd.DataFrame(prob)
    df.to_csv(TRANSITION, header = None)

# Create arrays for tags
def create_array(tags):
    # create 2d array
    row = len(tags)
    # initialize with smoothing factor
    prob = [[SMOOTH_FACTOR] * (row) for i in range(row + 1)]
    prob[1][0] = 'START'
    prob[0][0] = None


    row = 2
    for tag in tags:
        if (tag != 'START'):
            prob[row][0] = tag
            row += 1

    col = 1
    for tag in tags:
        if(tag != 'START'):
            prob[0][col] = tag
            col += 1

    return prob


if __name__ == '__main__':
    # open the training file
    with open(TRAIN, 'r')as rf:
        for line in rf:
            #initial tag
            comp_tags = ['START']
            # tokenize the sentence
            comp_tags.extend(regexp_tokenize(line, r'(?<=/)\w+'))
            # create and count pair tags
            count_tag_pair(comp_tags)
    # create the transition probabilities
    create_transition()

