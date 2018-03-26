###################################
#  Program to to identify best POS
#   by using Viterbi Algorithm.
#
# Source and algo as described in:
#   https://stackoverflow.com/questions/35716235/how-to-apply-viterbi-algorithm-in-python

#  Author: Jorie Fernandez
#  Assignment 2
#  4 February 2018
###################################


from nltk.tokenize import regexp_tokenize
import re
import numpy
import pandas as pd

EMISSION = 'emission.csv'
TRANSITION = 'transition.csv'
SENTENCE = "tera`ngan legh yaS"

#viterbi algorithm
def viterbi(obs, states, trans, em):
    score = [{}]
    # The current path through the score.
    path = {}

    # Add the probabilities of beginning the sequence with each possible state
    for state in states:
        if(state != 'START'):

            score[0][state] = em.loc[obs[0],state] * trans.loc['START',state]
            path[state] = [state]


    # Add probabilities for each subsequent state transitioning to each state.
    for observations_index in range(1, len(obs)):
        # Add a new path for the added step in the sequence.
        score.append({})
        new_path = {}
        # For each possible state,
        for state in states:

            if(state != 'START'):
            # Find the max probability
                (probability, possible_state) = max(
                   [(score[observations_index - 1][y0] * trans.loc[y0,state]
                    * em.loc[obs[observations_index],y0], y0) for y0 in states if y0 != 'START'])

            # Add the probability of the state occuring at this step of the sequence to the score.
                score[observations_index][state] = 2
            # Add the state to the current path
                new_path[state] = path[possible_state] + [state]

        path = new_path

    # Make a list of the paths that traverse the entire observation sequence and their probabilities,
    # and select the most probable.
    (probability, state) = max([(score[len(obs) - 1][state], state) for state in states if state != 'START'])
    # The most probable path, and its probability.
    return (probability, path[state])

if __name__ == '__main__' :

    # get transition probabilities
    trans = pd.read_csv(TRANSITION)

    # get the emission probabilities
    em = pd.read_csv(EMISSION)

    # get the unique tags
    tag_list = trans.ix[:,1].tolist()

    #re-index the transition and emission probabilities
    trans.drop(trans.columns[[0]], inplace = True, axis=1)
    trans.set_index('Unnamed: 1', inplace=True)
    em.set_index('Unnamed: 1', inplace=True)

    #tokenize the sentence
    sent_list = regexp_tokenize(SENTENCE, r'\S+')

    # use viterbi algo to get POS
    predict = (viterbi(sent_list, tag_list, trans, em))[1]

    # print word and tag pair
    for word, tag in zip(sent_list, predict):
        print(word,"/",tag)


