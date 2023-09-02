import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline, AutoTokenizer, PegasusForConditionalGeneration
import nltk

# function that returns summarized article
def summarize(article):
    model = PegasusForConditionalGeneration.from_pretrained("google/pegasus-xsum")
    tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
    # PEGASUS text summarizer
    ARTICLE_TO_SUMMARIZE = article
    inputs = tokenizer(ARTICLE_TO_SUMMARIZE, max_length=100, return_tensors="pt")

    # Generate Summary
    summary_ids = model.generate(inputs["input_ids"])
    return tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]

# function that plots histogram of length of content in list
def hist(summaries):
    summaryLength = []
    for i in range(len(summaries)):
        sentenceList = nltk.sent_tokenize(summaries[i])
        for j in range(len(sentenceList)):
            sentenceList[j] = nltk.word_tokenize(sentenceList[j])
        wordCount = 0
        for j in range(len(sentenceList)):
            wordCount = wordCount + len(sentenceList[j])
        summaryLength.append(wordCount)

    plt.hist(summaryLength)
    plt.show()

# read csv
df = pd.read_csv("news.csv")

# # plot histogram of summary length
# summary = df["Summary"].tolist()
# hist(summary)

# get full text
full_text = df["Full Text"].tolist()
pegasus_summary = []

for text in full_text:
    pegasus_summary.append(summarize(text))

df["PEGASUS Summary"] = pegasus_summary
df.to_csv('news.csv', index=False)

