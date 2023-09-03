import pandas as pd
from rouge_score import rouge_scorer
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

def mean(list):
    sum = 0;
    for item in list:
        sum = sum + item
    return sum / len(list)
df = pd.read_csv("news.csv")

summary = df["Summary"].tolist()
extracted_summary = df["Extracted Summary"].tolist()
pegasus_summary = df["PEGASUS Summary"].tolist()


extract_rouge_1 = []
extract_rouge_2 = []
extract_rouge_L = []
pegasus_rouge_1 = []
pegasus_rouge_2 = []
pegasus_rouge_L = []

for i in range(len(summary)):
    # summary vs extracted summary
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(summary[i], extracted_summary[i])

    extract_rouge_1.append(scores.get("rouge1").fmeasure)
    extract_rouge_2.append(scores.get("rouge2").fmeasure)
    extract_rouge_L.append(scores.get("rougeL").fmeasure)

    # summary vs pegasus summary

    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(summary[0], pegasus_summary[0])

    pegasus_rouge_1.append(scores.get("rouge1").fmeasure)
    pegasus_rouge_2.append(scores.get("rouge2").fmeasure)
    pegasus_rouge_L.append(scores.get("rougeL").fmeasure)

df["extract_rouge_1"] = extract_rouge_1
df["extract_rouge_2"] = extract_rouge_2
df["extract_rouge_L"] = extract_rouge_L
df["pegasus_rouge_1"] = pegasus_rouge_1
df["pegasus_rouge_2"] = pegasus_rouge_2
df["pegasus_rouge_L"] = pegasus_rouge_L

# # filtering and analysis of similarity between summaries
# filtered = df.copy()

# # extractive summary
# filtered_extractive = filtered[(filtered["extract_rouge_1"] > 0.6) 
#                                & (filtered["extract_rouge_2"] > 0.6) 
#                                & (filtered["extract_rouge_L"] > 0.6)]

# print(filtered_extractive["Summary"].tolist()[0])
# print(filtered_extractive["Extracted Summary"].tolist()[0])

# # abstractive summary
# filtered_abstractive = filtered[(filtered["pegasus_rouge_1"] > 0.6)
#                                 & (filtered["pegasus_rouge_2"] > 0.6)
#                                 & (filtered["pegasus_rouge_L"] > 0.6)]

# print(filtered_abstractive["Summary"].tolist()[0])
# print(filtered_abstractive["PEGASUS Summary"].tolist()[0])

# plotting histograms for rouge-1 scores for extractive and abstractive summary

# plt.hist(extract_rouge_1, alpha = 0.5)
# plt.hist(pegasus_rouge_2, alpha = 0.5)
# plt.show()

# checking mean of both scores
# print(mean(extract_rouge_1))
# print(mean(pegasus_rouge_1))

# conduct mann whitney u test for rouge 1, 2, L
print(mannwhitneyu(extract_rouge_1, pegasus_rouge_1, use_continuity = True, alternative = 'two-sided'))
print(mannwhitneyu(extract_rouge_2, pegasus_rouge_2, use_continuity = True, alternative = 'two-sided'))
print(mannwhitneyu(extract_rouge_L, pegasus_rouge_L, use_continuity = True, alternative = 'two-sided'))

# df.to_csv("news.csv", index = False)