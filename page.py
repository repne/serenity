from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import urlfetch
import hashlib

class Page(db.Model):
    url = db.TextProperty()

def get(key):
    url = memcache.get(key)
    if not url:
        page = Page.get_by_key_name(key)
        if page:
            url = page.url
            memcache.add(key, url)
    return url

def create(url):
    return hashlib.sha1(url).hexdigest()

def store(key, url):
    page = Page(key_name=key, url=url)
    page.put()

def resolve(url):
    original_url = url
    for i in xrange(10):
        try:
            if '#' in url:
                return url
            response = urlfetch.fetch(url, method='HEAD', follow_redirects=False)
            if response and response.status_code in (301, 302):
                original_url = url
                url = response.headers['Location']
            elif response and response.status_code in (200, 204, 405, 403, 404):
                return url
            else:
                return original_url
        except urlfetch.DownloadError:
            return original_url
        except urlfetch.InvalidURLError:
            return original_url
    return original_url
