# -*- coding: utf-8 -*-
from google.appengine.ext import ndb


class News3(ndb.Model):
    """  """
    title = ndb.TextProperty(indexed = True, repeated=False)
    subtitle = ndb.TextProperty(repeated=False)
    image = ndb.PickleProperty(repeated=False)
    url = ndb.TextProperty(indexed = True, repeated=False)
    category = ndb.TextProperty(repeated=False, indexed = True)
    keyword = ndb.JsonProperty(indexed = True)
    news_from = ndb.TextProperty(indexed = True)
    html = ndb.TextProperty()
    date = ndb.DateProperty(indexed = True, auto_now_add=True)
    synonym = ndb.JsonProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    id = ndb.IntegerProperty(indexed = True)
    hour = ndb.IntegerProperty(indexed = True)
    in_use = ndb.BooleanProperty(default = False)
    mine_category = ndb.TextProperty(repeated=False)


class NewsSelect2(ndb.Model):
    ''' '''
    title = ndb.TextProperty(indexed = True, repeated=False)
    subtitle = ndb.TextProperty(repeated=False)
    image = ndb.PickleProperty(repeated=False)
    url = ndb.TextProperty(repeated=False)
    category = ndb.TextProperty(repeated=False)
    news_from = ndb.TextProperty(indexed = True)
    html = ndb.TextProperty()
    similar = ndb.JsonProperty()
    cant_similar = ndb.IntegerProperty(indexed = True, default = 0)
    keyword_set = ndb.PickleProperty()
    keyword = ndb.JsonProperty()
    keys = ndb.JsonProperty()
    date = ndb.DateProperty(indexed = True, auto_now_add=True)
    is_similar = ndb.BooleanProperty()
    id = ndb.IntegerProperty(indexed = True)
    hour = ndb.IntegerProperty(indexed = True)
    created = ndb.DateTimeProperty(auto_now_add=True)


class News(ndb.Model):
    """  """
    title = ndb.TextProperty(indexed = True, repeated=False)
    subtitle = ndb.TextProperty(repeated=False)
    image = ndb.PickleProperty(repeated=False)
    url = ndb.TextProperty(repeated=False)
    category = ndb.TextProperty(repeated=False)
    keyword = ndb.JsonProperty()
    news_from = ndb.TextProperty(indexed = True)
    html = ndb.TextProperty()
    date = ndb.DateProperty(indexed = True, auto_now_add=True)
    synonym = ndb.JsonProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    id = ndb.IntegerProperty(indexed = True)
    hour = ndb.IntegerProperty(indexed = True)
    in_use = ndb.BooleanProperty(default = False)
    mine_category = ndb.TextProperty(repeated=False)


class NewsSelect(ndb.Model):
    ''' '''
    title = ndb.TextProperty(indexed = True, repeated=False)
    subtitle = ndb.TextProperty(repeated=False)
    image = ndb.PickleProperty(repeated=False)
    url = ndb.TextProperty(repeated=False)
    category = ndb.TextProperty(repeated=False)
    news_from = ndb.TextProperty(indexed = True)
    html = ndb.TextProperty()
    similar = ndb.JsonProperty()
    cant_similar = ndb.IntegerProperty(indexed = True, default = 0)
    keyword_set = ndb.PickleProperty()
    keyword = ndb.JsonProperty()
    keys = ndb.JsonProperty()
    date = ndb.DateProperty(indexed = True, auto_now_add=True)
    is_similar = ndb.BooleanProperty()
    id = ndb.IntegerProperty(indexed = True)
    hour = ndb.IntegerProperty(indexed = True)
    created = ndb.DateTimeProperty(auto_now_add=True)


class Category(ndb.Model):
    """  """
    name = ndb.TextProperty(indexed = True, repeated=False)
    keyword = ndb.JsonProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)


class Horoscopos(ndb.Model):
    """  """
    url = ndb.TextProperty(indexed = True, repeated=False)
    signo = ndb.TextProperty(indexed = True, repeated=False)
    horoscopo = ndb.TextProperty()
    image = ndb.TextProperty()
    date = ndb.DateProperty(indexed = True, auto_now_add=True)
    created = ndb.DateTimeProperty(auto_now_add=True)


class Frequencies(ndb.Model):
    """  """
    frequencies = ndb.JsonProperty()
    id = ndb.IntegerProperty(indexed = True)


class Comentarios(ndb.Model):
    """  """
    nombre = ndb.TextProperty(indexed = True, repeated=False)
    email = ndb.TextProperty(indexed = True, repeated=False)
    comentario = ndb.TextProperty(indexed = True, repeated=False)
    date = ndb.DateProperty(indexed = True, auto_now_add=True)
    created = ndb.DateTimeProperty(auto_now_add=True)