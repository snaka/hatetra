# coding: utf-8
# 
# main.py
#
# imports {{{
import os
import md5
import random
import urllib
import logging
import hashlib
import yaml

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
from google.appengine.api import urlfetch
from google.appengine.api import users

from models.account import *

# }}}

class MainHandler(webapp.RequestHandler):

    def get(self):
        values = { 'link_to_login' : users.create_login_url("/register")}
        path = os.path.join(os.path.dirname(__file__), "views/top.html")
        self.response.out.write(template.render(path, values))

    def post(self):
        """
            Handle Webnotification
        """

        # verify users key
        user_hash = self.request.path[1:]
        user_key = self.request.get("key")
        logging.debug("user_hash: %s" % user_hash)
        logging.debug("user_key : %s" % user_key)
        if not Account.get_key_by_hash(user_hash) == user_key:
            logging.debug("invalid key")
            self.response.out.write("Invalid key error")
            return

        # verify status
        status   = self.request.get("status")
        logging.debug("status: %s" % status)
        if status != "favorite:add":
            logging.debug("ignore status: %s" % status)
            self.response.out.write("OK(but, ignore)")
            return

        # notify
        username = self.request.get("username")
        title    = self.request.get("title")
        comment  = self.request.get("comment") or " "
        url      = self.request.get("url")
        logging.debug("user: %s, title: %s, comment: %s" % (username, title, comment))
        res = notify(user_hash, username, title, comment, url)

        self.response.out.write(res.content)


class RegisterHandler(webapp.RequestHandler):

    def get(self):
        """
            Register/Confirm user's account
        """
        user = users.get_current_user()
        [notify_key, user_hash] = Account.get_key(user)

        if not notify_key:
            [notify_key, user_hash] = Account.generate_key(user)

        logout_url = users.create_logout_url("/")

        values = { 'user_name'      : user,
                   'user_hash'      : user_hash,
                   'notify_key'     : notify_key,
                   'link_to_logout' : logout_url }
        path = os.path.join(os.path.dirname(__file__), "views/register.html")
        self.response.out.write(template.render(path, values))

    def post(self):
        """
            Update key
        """
        user = users.get_current_user()
        Account.generate_key(user)
        self.redirect("/register")


def notify(user_hash, username, title, comment, url):
    apikey = get_apikey()
    prefix = username[0:2]

    body = {'title' : (u"%s" % username).encode('utf-8'),
            'text'  : (u"「%s」\n%s" % (title, comment)).encode('utf-8'),
            'icon'  : "http://www.hatena.ne.jp/users/%s/%s/profile.gif" % (prefix, username),
            'link'  : (u"%s" % url).encode('utf-8')}
    encoded_body = urllib.urlencode(body)

    url = "http://api.notify.io/v1/notify/%s?api_key=%s" % (user_hash, apikey)
    logging.debug("notify url: %s" % url)
    res = urlfetch.fetch(url, 
                         payload = encoded_body,
                         method = urlfetch.POST,
                         deadline = 10)
    return res

def get_apikey():
    f = open(os.path.join(os.path.dirname(__file__), "secret.yaml"))
    secret = yaml.load(f)
    f.close()
    return secret['apikey']

def main():
  application = webapp.WSGIApplication([('/register',   RegisterHandler), 
                                        ('/.*',         MainHandler)],
                                       debug=True)
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()

# vim: sw=4 ts=4 et fdm=marker
