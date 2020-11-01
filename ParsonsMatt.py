from Model import *
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
import requests

blog = Blog("https://www.parsonsmatt.org/", "Overcoming Software", "FP, Haskell")

def parse_article(article_container):
        link = article_container.find("a")
        timestamp = date_parser.parse(article_container.find("time").get_text())
        url = blog.url + link.get("href")
        return Article(blog, url, link.get_text(), timestamp)

def get_articles():
    page = requests.get(blog.url)
    soup = BeautifulSoup(page.content, "html.parser")
    article_containers = soup.find_all("div", class_="list-item")
    return list(map(parse_article, article_containers))
