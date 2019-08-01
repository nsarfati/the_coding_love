#!/usr/local/bin/python

import io
import os
import requests
import feedparser
import urllib2
import traceback

from datetime import datetime
from time import sleep, mktime
from slackclient import SlackClient
from BeautifulSoup import BeautifulSoup
from requests_toolbelt.multipart.encoder import MultipartEncoder

# REMEMBER TO CONFIGURE
BOT_TOKEN = '<FILL_ME_WITH_SLACK_BOT_TOKEN>'
THE_CODING_LOVE_CHANNEL = '#the_coding_love' # Slack channel, by default it's called #the_coding_love

FEED_URL = 'http://thecodinglove.com/rss'

DEFAULT_TIMEOUT = 5
SLEEP_TIME = 10
PROCESSED_URLS_FILE_NAME = './the_coding_love_lines'

slack_client = SlackClient(BOT_TOKEN)

def load_processed_urls():
    processed_urls = []

    if (os.path.exists(PROCESSED_URLS_FILE_NAME)):
        with open(PROCESSED_URLS_FILE_NAME, 'r') as f:
            content = f.readlines()

        processed_urls = [l.strip() for l in content]

    return processed_urls


def dump_processed_url(url):
    f = open(PROCESSED_URLS_FILE_NAME, 'a')
    f.write(str(url) + '\n')

    f.close()


def process_entries(processed_urls, entries):
    for e in entries[::-1]:
        link = str(e['link']).strip()

        if (link not in processed_urls):
            image_link = get_image_url(link)

            if (image_link is not None):

                # Temporary fix since SSL is not correct
                image_link = image_link.replace('https', 'http')

                r = urllib2.urlopen(image_link, timeout=DEFAULT_TIMEOUT)
                gif_content = r.read()

                slack_client.api_call("files.upload",
                        title=e['title'],
                        channels=THE_CODING_LOVE_CHANNEL,
                        filetype='thumb_360_gif',
                        file=io.BytesIO(requests.get(image_link).content))

                print "Image[%s] sent for post[%s]" % (str(image_link), link)

                processed_urls.append(link)
                dump_processed_url(link)


def get_image_url(link):
    try:
        return str(BeautifulSoup(requests.get(link).content).find('object')['data']).strip()
    except Exception as e:
        return None


if __name__ == "__main__":

    try:
        feed = feedparser.parse(FEED_URL)

        process_entries(load_processed_urls(), feed['entries'])
    except Exception as e:
        print "Error produced trying to process feed error[%s]" % str(e)
        traceback.print_exc()