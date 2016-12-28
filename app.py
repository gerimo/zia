
# -*- coding: utf-8 -*- 
import random
import string
import cherrypy
import os
from pymongo import MongoClient
from datetime import datetime
from pprint import pprint
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

class FrontEnd(object):
    @cherrypy.expose
    def index(self):
        html = open("frontend/index.html").read()
        return html

    @cherrypy.expose
    def create(self):
        client = MongoClient()
        db = client.cherrypies        
        result = db.users.insert_one(
    {
            "id": "5",
            "name": "Ricardo Rimoldi",
            "email": "surimo@fibertel.com.ar",
            "address": "De la Angostura 63",
            "telephone": "+54 911 44004075",
            "company_name": "Inmobi"
    })  

# a la database le puse de nombre "cherrypies"
    @cherrypy.expose
    def db(self, id = 1):
        brand = "Zia"
        client = MongoClient()
        db = client.cherrypies        
        c = db.users.find({"id":id})
        for document in c: 
            email = document["email"]
            name = document["name"]
            company_name = document["company_name"]
            telephone = document["telephone"]
            address = document["address"]
        template = open("templates/a/template.html").read()
        return template.format(email=email,name=name,company_name=company_name,telephone=telephone,address=address,brand=brand)
    

    @cherrypy.expose
    def user(self):
        client = MongoClient()
        db = client.cherrypies        
        result = db.users.insert_one(
    {
            "id": id,
            "name": name,
            "email": email,
            "address": address,
            "company_name": company_name,
            "telephone": telephone
    })  
        user = open("frontend/user.html").read()
        return user 

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './frontend/public'
        },
        '/route': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './templates/a'
        }	
    }
    cherrypy.quickstart(FrontEnd(), '/', conf)
