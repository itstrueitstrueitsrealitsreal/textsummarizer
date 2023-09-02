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
full_text = []

# iterate through 50 pages
for i in range(50):
    # get url for page
    URL = "https://www.newsweek.com/newsfeed?page=" + str(i + 1)

    r = requests.get(url = URL, headers = headers)

    soup = bs4.BeautifulSoup(r.content, "lxml")

    articles = soup.find_all("article")
    # iterate through 30 articles on a single page, isolating their content
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

# iterate through list of urls to obtain content of articles
for link in url:
    r = requests.get(url = link, headers = headers)
    soup = bs4.BeautifulSoup(r.content, "lxml")

    body = soup.find("div", class_ = "article-body")

    paras = body.find_all("p")

    content = ""
    for para in paras:
        content = content + para.text + " "
    content = content[:-1]
    full_text.append(content)

data = {"Category": category,
        "URL": url,
        "Title": title,
        "Summary": summary,
        "Full Text": full_text}

df = pd.DataFrame(data)
df.to_csv('news.csv', index=False)