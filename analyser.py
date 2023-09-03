import pandas as pd
from rouge_score import rouge_scorer
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

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
    scores = scorer.score(summary[0], extracted_summary[0])

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

# filtered = df.copy()

# filtered = filtered.iloc[:, 7:]
# filtered = filtered[(filtered.extract_rouge_1 > 0.6) 
#                     & (filtered.extract_rouge_2 > 0.6) 
#                     & (filtered.extract_rouge_L > 0.6) 
#                     & (filtered.pegasus_rouge_1 > 0.6)
#                     & (filtered.pegasus_rouge_2 > 0.6)
#                     & (filtered.pegasus_rouge_L > 0.6)]
# print(filtered)
# df.filter()

print(df)

df.to_csv("news.csv", index = False)