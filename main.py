from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api import taskqueue

import page

class LookupHandler(webapp.RequestHandler):
    def get(self, key):
        if key and len(key):
            url = page.get(key)
            if url:
                return self.redirect(url, permanent=True)
        self.response.set_status(404)

class InsertHandler(webapp.RequestHandler):
    def post(self):
        url = self.request.get('url')
        if url and len(url):
            deferred = self.request.get('deferred')
            key = page.create(url)
            if not deferred:
                url = page.resolve(url)
                if url:
                    page.store(key, url)
            else:
                taskqueue.add(url='/deferred', params=dict(url=url, key=key))

            if key and url:
                self.response.set_status(201)
                self.response.headers['Location'] = '%s/%s' % (self.request.host_url, key)
                self.response.clear()
            else:
                self.response.set_status(404)
        else:
            self.response.set_status(400)

class DeferredInsertHandler(webapp.RequestHandler):
    def post(self):
        url = self.request.get('url')
        key = self.request.get('key')
        final_url = page.resolve(url)
        if final_url:
            page.store(key, final_url)
        else:
            import logging
            logging.info('Error on url %s' % url)
            self.response.set_status(404)

def main():
    routes = [
        ('/', InsertHandler),
        ('/deferred', DeferredInsertHandler),
        ('/(\w+)', LookupHandler),
    ]
    application = webapp.WSGIApplication(routes, debug=False)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
