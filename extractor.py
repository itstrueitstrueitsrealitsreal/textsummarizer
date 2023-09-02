import pandas as pd
import numpy as np
import nltk
import re
import ssl
import string

def remove_punctuation(input_string):
    # Make a regular expression that matches all punctuation
    regex = re.compile('[%s]' % re.escape(string.punctuation))
    # Use the regex
    return regex.sub('', input_string)

# download punkt
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("punkt")

# read csv
df = pd.read_csv("news.csv")


# get full text 
texts = df["Full Text"].tolist()

extracted_summary = []

for text in texts:

    tokens = nltk.sent_tokenize(text, language = 'english')
    sentences = tokens.copy()
    for i in range(len(tokens)):
        # change all sentences to lowercase
        tokens[i] = tokens[i].lower()
        # remove all punctuation from sentences
        tokens[i] = remove_punctuation(tokens[i])
        # tokenize sentences into words, getting list of list of words
        tokens[i] = nltk.word_tokenize(tokens[i])

    # create and update word dict with frequency of occurence of words 

    word_dict = {}

    for i in range(len(tokens)):
        for j in range(len(tokens[i])):
            # check if word is already in dict
            if (word_dict.get(tokens[i][j])):
                word_dict.update({tokens[i][j]: word_dict.get(tokens[i][j]) + 1})
            else:
                word_dict.update({tokens[i][j]: 1})

    # iterate through list of sentences, obtain sentence with highest weight
    sentence_weights = []

    for i in range(len(tokens)):
        weight = 0
        for word in tokens[i]:
            weight = weight + word_dict.get(word)
        sentence_weights.append(weight)

    # obtain the indices of the two sentences with the highest weights
    indices = np.array(sentence_weights).argsort()[::-1][:2]

    # store two sentences with highest weights 
    toptwo = ""
    for idx in indices:
        toptwo = toptwo + str(sentences[idx]) + " "

    extracted_summary.append(toptwo)

df["Extracted Summary"] = extracted_summary
df.to_csv('news.csv', index=False)