# Estamos usando un sevidor HTTP que viene incluido en el framwork de Cherrypy
# Usamos como base de datos MONGODB. La base de datos se llama "cherrypies".

# -*- coding: utf-8 -*- 
import random
import json
import string
import cherrypy
import os
from pymongo import MongoClient
from datetime import datetime
from pprint import pprint
from bson.objectid import ObjectId
from collections import namedtuple #esto permite traer los resultados de las queries como instancias de objetos.
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')

class FrontEnd(object):
    @cherrypy.expose
    def index(self):
        brand = "Zia"
        html = open("frontend/index.html").read()
        return html

# Paso 0: carga manual de datos de prueba en la base de datos
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

# Paso 1: crear un usuario desde la vista.
    @cherrypy.expose
    def register_user(self, email, company_name, company_email, company_telephone, company_address):
        client = MongoClient()
        db = client.cherrypies        
        result = db.users.insert_one({
            "email": email,
            "password": "",
            "company": {
                "name": company_name,
                "email": company_email,
                "telephone": company_telephone,
                "address": company_address
                }
    })  
        template = open("templates/a/template.html").read()
        return "Gracias por registrarte"

# Paso 2: Generar vista del template con email de la empresa del usuario
    @cherrypy.expose
    def template1(self):
        client = MongoClient()
        db = client.cherrypies        
        c = db.users.find({"company.email":"alianzas@sigur.cl"})
        for document in c:
            email = document["email"]
            company_name = document["company"]["name"]
            company_email = document["company"]["email"]
            company_telephone = document["company"]["telephone"]
            company_address = document["company"]["address"]          
        template = open("templates/a/template.html").read()
        return template.format(email=email,company_name=company_name,company_email=company_email,company_telephone=company_telephone,company_address=company_address)

    # Se pueden ver los resultados ingresando http://localhost:9090/template?design=a&email=alianzas@sigur.cl
    @cherrypy.expose
    def template(self, design, email):
        client = MongoClient()
        db = client.cherrypies        
        cursor = db.users.find({"company.email":email})
        Company = namedtuple('company', 'email name telephone address')
        User = namedtuple('User', 'email, company') #uso namedtuple para llamar los resultados como objetos con notacion con puntos, como: "company.email"
        for row in cursor:
            user = User(row['email'], Company(row['company']['email'],row['company']['name'],row['company']['telephone'],row['company']['address'])) #esta es la sintaxis necesaria para usar nametupe
        if design == "a":
            route = "templates/a/1.html"
        else:
            route = "templates/b/1.html"
        template = open(route).read()
        return template.format(user=user,design=design)

if __name__ == '__main__':
    # Rutas y configuraciones adicionales
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
