from google.appengine.ext import ndb

class Sporocilo(ndb.Model):
    besedilo_sporocila = ndb.StringProperty()
    email = ndb.StringProperty()
    poslano = ndb.DateTimeProperty(auto_now_add= True)
    avtor = ndb.StringProperty()