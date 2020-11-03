import datetime
import itertools

import ParsonsMatt
import TomHarding

def get_news_feed(articles, after):
    new_articles = filter(lambda a: a.timestamp > after, articles)
    grouped_articles = itertools.groupby(new_articles, lambda a: a.blog)
    feed = ["<h1>News feed since {0}</h1>".format(after)]
    for blog, articles in grouped_articles:
        feed.append("<h2>{0} ({1})</h2>".format(blog.name, blog.description))
        feed.append("<ul>")
        for article in articles:
            feed.append('<li><a href="{0}">{1}</a></li>'.format(article.url, article.name))
        feed.append("</ul>")
    
    return "\n".join(feed)

articles = list(itertools.chain.from_iterable([
    ParsonsMatt.get_articles(),
    TomHarding.get_articles()
]))

week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
news_feed = get_news_feed(articles, after=week_ago)
print(news_feed)
