# coding: utf-8

import md5
import random
import logging
import hashlib

from google.appengine.ext import db
from google.appengine.api import users

class Account(db.Model):
    user = db.UserProperty(required = True)
    users_key  = db.StringProperty(required = True)
    user_hash  = db.StringProperty()

    @classmethod
    def generate_key(cls, user):
        q = db.Query(Account)
        q.filter("user", user)
        acc = q.get()

        key = cls.create_key()

        if acc:
            logging.debug("*Re*generate key for %s" % user)
            acc.users_key = key
            acc.put()

        else:
            logging.debug("Generate key for %s" % user)
            acc = Account(user  = user,
                          users_key = key,
                          user_hash = hashlib.md5(user.email()).hexdigest())
            acc.put()

        return [acc.users_key, acc.user_hash]

    @classmethod
    def get_key(cls, user):
        q = db.Query(Account)
        q.filter("user", user)
        acc = q.get()
        if acc:
            return [acc.users_key, acc.user_hash]
        return [None, None]


    @classmethod
    def get_key_by_hash(cls, hash):
        q = db.Query(Account)
        q.filter("user_hash", hash)
        acc = q.get()
        if acc:
            return acc.users_key
        return None

    @classmethod
    def create_key(cls):
        return hashlib.md5(str(random.random())).hexdigest()[:6]

