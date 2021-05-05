import requests
from bs4 import BeautifulSoup
import string
import os


def nature_url(relative_url):
    if relative_url:
        return 'https://www.nature.com' + relative_url


n_pages = int(input()) + 1
wanted_article_type = input()
page_url = r'https://www.nature.com/nature/articles'
i = 1
while i < n_pages and page_url:
    page_dir = 'Page_' + str(i)
    os.mkdir(page_dir)
    r = requests.get(page_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    page_url = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        articles = soup.find_all('article')
        page_url = nature_url(soup.find('li', {'data-page': 'next'}).
                              find('a').get('href'))
        for article in articles:
            if article.find('span', {'class': "c-meta__type"}).text \
                    == wanted_article_type:
                link = article.find('a').get('href')
                title = article.find('h3').text.strip()
                for p in string.punctuation:
                    title = title.replace(p, '')
                title = title.replace(' ', '_')
                article_resp = requests.get(nature_url(link))
                if article_resp:
                    s = BeautifulSoup(article_resp.content, 'html.parser')
                    body = s.find('div', {'class': 'article-item__body'}) \
                           or s.find('div', {'class': 'article__body'})
                    if body:
                        with open(os.path.join(page_dir, title + '.txt'), 'wb') as f:
                            f.write(body.text.strip().encode())
    i += 1
