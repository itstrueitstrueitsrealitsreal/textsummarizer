import requests
import bs4
import pandas as pd
from fake_useragent import UserAgent

# create ua for generating fake user-agent field
ua = UserAgent()
headers = {'User-Agent': ua.random}

category = []
url = []
title = []
summary = []

for i in range(50):
    # get url for page
    URL = "https://www.newsweek.com/newsfeed?page=" + str(i + 1)

    r = requests.get(url = URL, headers = headers)

    soup = bs4.BeautifulSoup(r.content, "lxml")

    articles = soup.find_all("article")
    for article in articles:
        # obtaining category
        categoryTag = article.find("div", class_ = "category")
        if (categoryTag):
            category.append(article.find("div", class_ = "category").get_text())
        else:
            category.append("None")
        # obtaining path
        path = article.find("a", href = True, class_ = "zero")
        # obtaining URL
        articleURL = "https://www.newsweek.com" + str(path["href"])
        url.append(articleURL)
        # obtaining title
        title.append(article.find("h3").get_text())
        # obtaining summary
        summary.append(article.find("div", class_ = "summary").get_text())


data = {"Category": category,
        "URL": url,
        "Title": title,
        "Summary": summary}

df = pd.DataFrame(data)
df.to_csv('News.csv', index=False)
print(df)