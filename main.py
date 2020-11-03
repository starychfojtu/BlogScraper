import datetime
import itertools
import requests

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

def send_email(content):
	return requests.post(
		"https://api.mailgun.net/v3/sandboxb243fe7e7f9d437099b9d7aa678f0b7f.mailgun.org/messages",
		auth=("api", "API_KEY"),
		data={
            "from": "Mailgun Sandbox <postmaster@sandboxb243fe7e7f9d437099b9d7aa678f0b7f.mailgun.org>",
			"to": "email@gmail.com",
			"subject": "Weekly news feed",
			"html": content
        }
    )

articles = list(itertools.chain.from_iterable([
    ParsonsMatt.get_articles(),
    TomHarding.get_articles()
]))

week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
news_feed = get_news_feed(articles, after=week_ago)
print(news_feed)

print(send_email(news_feed).content)