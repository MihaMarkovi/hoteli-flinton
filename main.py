#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class PlusHandler(BaseHandler):
    def post(self):
        plus_1 = self.request.get("plus_1")
        plus_2= self.request.get("plus_2")
        rezultat_plus = int(plus_1) + int(plus_2)
        params = {"rezultat_plus": rezultat_plus}
        return self.render_template("plus.html", params=params)
        self.write(rezultat_plus)

class OsnovnaStran(BaseHandler):
    def get(self):
        return self.render_template("base.html")

class AboutHandler(BaseHandler):
    def get(self):
        return self.render_template("about.html")

class SporocilaHandler(BaseHandler):
    def get(self):

        sporocila = Sporocilo.query().fetch()

        params ={"sporocila": sporocila}

        self.render_template("vsa_sporocila.html", params=params)

class ContactHandler(BaseHandler):
    def get(self):
        return self.render_template("contact.html")

class RezultatHandler(BaseHandler):
    def post(self):
        besedilo = self.request.get("sporocilo")
        email = self.request.get("email")
        ime = self.request.get("ime")
        if len(ime) == 0:
            ime = "neznanec"
        sporocilo = Sporocilo(besedilo_sporocila=besedilo, email=email, avtor=ime)
        sporocilo.put()

        return self.render_template("rezultat.html")

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):

        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params ={"sporocilo": sporocilo}
        return self.render_template("posamezno_sporocilo.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/plus', PlusHandler),
    webapp2.Route('/mywebside.html', OsnovnaStran),
    webapp2.Route('/about', AboutHandler),
    webapp2.Route('/contact', ContactHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/vsa_sporocila', SporocilaHandler),
    webapp2.Route('/sporocila/<sporocilo_id:\d+>',PosameznoSporociloHandler)
], debug=True)
