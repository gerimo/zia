# Estamos usando un sevidor HTTP que viene incluido en el framwork de Cherrypy
# Usamos como base de datos MONGODB. La base de datos se llama "cherrypies".

# -*- coding: utf-8 -*- 
import random
import string
import cherrypy
import os
from pymongo import MongoClient
from datetime import datetime
from pprint import pprint
from bson.objectid import ObjectId
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

class FrontEnd(object):
    @cherrypy.expose
    def index(self):
        html = open("frontend/index.html").read()
        return html

    @cherrypy.expose
    def popa(self):
        client = MongoClient()
        db = client.cherrypies        
        c = db.users.find({"email":"surimo@fibertel.com.ar"})
        for document in c:
            company_name = document["company"]["name"]
            company_email = document["company"]["email"]
            company_telephone = document["company"]["telephone"]
            company_address = document["company"]["address"]          
        return (company_name)

# carga manual de datos de prueba en la base de datos
    @cherrypy.expose
    def create(self):
        client = MongoClient()
        db = client.cherrypies        
        result = db.users.insert_one(
    {
            "email": "surimo@fibertel.com.ar",
            "password": "pass",
            "company": {
                "name": "Inmobi",
                "email": "alianzas@sigur.cl",
                "telephone": "+54 911 44004075",
                "address": "De la Angostura 63"
                }
    })  
        return "Objeto creado"

# vista del template a, para un usuario dado.
    @cherrypy.expose
    def template(self, email = "alianzas@sigur.cl"):
        client = MongoClient()
        db = client.cherrypies        
        c = db.users.find({"company.email":email})
        for document in c: 
            email = document["email"]
            blas = document["telephone"]
        template = open("templates/a/1.html").read()
        return template.format(blas = blas)

# vista del template a, para un usuario dado.
    
    class Company(object):
        def __init__(self, name, email, telephone, address):
            self.name = name
            self.email = email
            self.telephone = telephone
            self.address = address
        company = Company()

    @cherrypy.expose
    def template1(self):
        client = MongoClient()
        db = client.cherrypies        
        c = db.users.find({"email":"surimo@fibertel.com.ar"})
        for document in c:
            company_name = document["company"]["name"]
            company_email = document["company"]["email"]
            company_telephone = document["company"]["telephone"]
            company_address = document["company"]["address"]          
        return (company_name)

# Variables comunes, para mostrar el template antes de tener     
    @cherrypy.expose
    def template_a(self, id = 1):
        email = "soporte@tuempresa.cl"
        name = "Jose Lopez"
        company_name = "Tu empresa"
        telephone = "22 100 1000"
        address = "Tu direccion 100"
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
        user = open("frontend/user.html").read()
        return user

    @cherrypy.expose
    def register_user(self,id,name,email,address,company_name,telephone):
        name = name
        id = id
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
        template = open("templates/a/template.html").read()
        return template.format(id = id,name=name,email=email,company_name=company_name,telephone=telephone,address=address)
    

    @cherrypy.expose
    def register_user1(self,name,email,address,company_name,telephone):
        client = MongoClient()
        db = client.cherrypies        
        result = db.users.insert_one(
    {
            "email": email,
            "password": password,
            "company": {
                "name": name,
                "email": email,
                "telephone": "+54 911 44004075",
                "address": "De la Angostura 63"
                }
    })  
    

if __name__ == '__main__':
    # Estamos usando un sistema de templates que se llama Jinja2 plugin
    from jinja2 import Template

    # Paths y configuraciones adicionales
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
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
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.quickstart(FrontEnd(), '/', conf)
