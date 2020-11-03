import datetime
import itertools
import smtplib
import ssl

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

def send_gmail(sender_email, password, receiver_email, subject, content):
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    message.attach(MIMEText(content, "html"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

articles = list(itertools.chain.from_iterable([
    ParsonsMatt.get_articles(),
    TomHarding.get_articles()
]))

week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
news_feed = get_news_feed(articles, after=week_ago)
print(news_feed)

send_gmail("your_mail@gmail.com", "pass_here", "receiver_mail@gmail.com", "Weekly news feed", news_feed)