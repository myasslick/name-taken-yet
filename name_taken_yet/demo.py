from name_taken_yet.check_youtube import youtube_search
from name_taken_yet.check_gmail import check_account_exists as gmail_search

import sys

query = sys.argv[1]

def list_channels(query, channels):
    print("<h4>Query (YouTube): <u>{q}</u></h4>".format(q=query))
    if channels["exact"]:
        print("<p>Matched? <b>{c}</b></p>".format(c=len(channels["exact"])))
        print("<ul>")
        for i, c in enumerate(channels["exact"]):
            title = c["channel_title"]
            id = c["channel_id"]
            print("<li><a href='https://www.youtube.com/channel/{id}'>{t}</a>".format(
                    id=id, t=title))
        print("</ul>")
    else:
        print("<p>Matched: <b>{c}</b></p>".format(c=0))
    if channels["similar"]:
        print("<p>Found similar:</p>")
        print("<ul>")
        for i, x in enumerate(channels["similar"]):
            try:
                title = x["channel_title"].encode('utf-8')
                id = x["channel_id"]
                print("<li><a href='https://www.youtube.com/channel/{id}'>{t}</a>".format(
                        id=id, t=title))
            except UnicodeEncodeError:
                title = x["channel_title"].encode('utf-8')
                id = x["channel_id"]
                print("<li><a href='https://www.youtube.com/channel/{id}'>{t}</a>".format(
                        id=id, t=title))
                continue
        print("</ul>")

specs = ["", "+", ".", "_"]
candidates = []

print("<h4>Query (Gmail): <u>{q}</u></h4>".format(q=query))
if " " in query:
    parts = query.split(" ")
    print("<ul>")
    for x in specs:
        new_query = "{x}".format(x=x).join(parts)
        existed = gmail_search(new_query)
        print("<li>Query: {q}@gmail.com taken? {e}</li>".format(e=existed["existed"], q=new_query))
    print("</ul>")
else:
    print("<ul>")
    existed = gmail_search(query)
    print("<li>Query: {q}@gmail.com taken? {e}</li>".format(q=query, e=existed["existed"]))
    print("</ul>")

results = youtube_search(query)
list_channels(query, results)
