import pandas as pd
from rouge_score import rouge_scorer
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

df = pd.read_csv("news.csv")

scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
scores = scorer.score('The quick brown fox jumps over the lazy dog',
                      'The quick brown dog jumps on the log.')

print(scores)