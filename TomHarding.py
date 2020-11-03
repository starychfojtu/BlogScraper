from Model import *
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
import requests

blog = Blog("http://www.tomharding.me/", "Tom Harding", "Category/Type Theory")

def parse_article(article_container):
    title_link = article_container.find("h2", class_="post-title").find("a")
    timestamp = date_parser.parse(article_container.find("span", class_="post-date").get_text())
    url = blog.url + title_link.get("href")
    return Article(blog, url, title_link.get_text(), timestamp)

def get_articles():
    page = requests.get(blog.url)
    soup = BeautifulSoup(page.content, "html.parser")
    article_containers = soup.find_all("article", class_="post")
    return list(map(parse_article, article_containers))
