Fernandez, Jorie
TCSS 456 Programming Assignment 1
Language Models

This program uses the following files:
1. Training file - doyle-27.txt
2. Test file - doyle-case-27.txt

Perplexities of the Models:
Based from the result, the perplexities of some sentences using the unigram and bigram models were not computed due
to the existence of unknown words. These words resulted to zero probability. This is opposed to the add-k smooth model
where each sentences where evaluated with perplexity number.

Looking at the computed perplexities of the sentences, the unigram model contains the sentence with the highest
perplexity of 5844, followed by the smooth model with 3952. The bigram model was only able to come up with a perplexity
value of 1 but majority of the sentences have undefined perplexities.

Therefore, we can say that unigram model performed the worse because of its high perplexity number. This is because with
just one word, it is hard to extract dependency or order of other words. Therefore, it is hard to predict what the next
associated word is.

Bigram Smoothing:
While the smoothing helped reducing the data sparsity of the bigram model in the sample data, it resulted to a higher
perplexity. This could be because there is a great number of unseen words in the test data that it assigned too much
probability mass to these words.

