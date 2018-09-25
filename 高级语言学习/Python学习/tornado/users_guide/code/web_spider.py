# -*- coding: utf-8 -*-

import time
from datetime import timedelta

from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag

from tornado import gen, httpclient, ioloop, queues

base_url = 'http://www.tornadoweb.org/en/stable'
concurrent = 200

async def get_links_from_url(url):
    '''Download the page at `url` and parse it for links.

    Returned links have had the fragment after '#' removed, and have been made absolute so, e.g. the URL 'gen.html#tornado.gen.coroutine' becomes 'http://www.tornado.org/en/stable/gen.html'
    '''
    resp = await httpclient.AsyncHTTPClient().fetch(url)
    print('fetch %s finish'%url)
    html = resp.body.decode(errors='ignore')
    return [ urljoin(url, remove_fragment(new_url)) for new_url in get_links(html) ]

def remove_fragment(url):
    pure_url, frag = urldefrag(url)
    return pure_url

def get_links(html):

    class URLSeeker(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.urls = list()

        def handle_starttag(self, tag, attrs):
            href = dict(attrs).get('href')
            if href and tag == 'a':
                self.urls.append(href)

    url_seeker = URLSeeker()
    url_seeker.feed(html)
    return url_seeker.urls

async def main():
    q = queues.Queue()
    start = time.time()
    fetching, fetched = set(), set()

    async def fetch_url(current_url):
        if current_url in fetching:
            return

        print('fetching %s'%current_url)
        fetching.add(current_url)
        urls = await get_links_from_url(current_url)
        fetched.add(current_url)

        for new_url in urls:
            if new_url.startswith(base_url):
                await q.put(new_url)

    async def worker():
        async for url in q:
            if url is None:
                return
            try:
                await fetch_url(url)
            except Exception as e:
                print('Exception: %s %s'%(e, url))
            finally:
                q.task_done()

    await q.put(base_url)

    workers = gen.multi([
        worker() for _ in range(concurrent)
    ])

    await q.join(timeout=timedelta(seconds=300))
    assert fetching == fetched
    print('Done in %ds, fetched %d URLs'%(time.time()-start, len(fetched)))

    for _ in range(concurrent):
        await q.put(None)

    await workers

if __name__ == "__main__":
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(main)
