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
    name = "Zucar"
    telephone = "22 938 1010"
    address = "La Concepcion 81"
    commune = "Providencia"
    city = "Santiago"
    country = "Chile"

# Vistas basicas 
    @cherrypy.expose
    def index(self):
        header = open('frontend/header.html').read()
        nav = open('frontend/nav.html').read() 
        body = open('frontend/index.html').read()
        footer = open('frontend/footer.html').read()
        return header.format(),nav.format(our=FrontEnd),body.format(our=FrontEnd),footer.format(our=FrontEnd)

# Paso 0: carga manual de datos de prueba en la base de datos
    @cherrypy.expose
    def create(self):
        client = MongoClient()
        db = client.cherrypies        
        result = db.users.insert_one(
    {
            "email": "email@email.com",
            "telephone": "22 200 2000",
            "password": "",
            "company": {
                "name": "Tu Empresa",
                "email": "soporte@tuempresa.cl",
                "telephone": "22 200 2000",
                "address": "Tu Direccion Comercial 100"
                }
    })  
        return "Objeto creado"

# Paso 1: crear un cliente desde la vista princial.
    @cherrypy.expose
    def user(self, email, telephone):
        header = open('frontend/header.html').read()
        body = open('frontend/company.html').read()
        footer = open('frontend/footer.html').read()
        cherrypy.session["email"] = email
        cherrypy.session["telephone"] = telephone
        return header.format(),body.format(our=FrontEnd),footer.format(our=FrontEnd)

# Paso 2: crear un cliente desde una vista.
    @cherrypy.expose
    def company(self, company_name, company_email, company_telephone):
        email = cherrypy.session["email"]
        telephone = cherrypy.session["telephone"]
        client = MongoClient()
        db = client.cherrypies 
        result = db.users.insert_one({
            "email": email,
            "telephone": telephone,
            "password": "",
            "company": {
                "name": company_name,
                "email": company_email,
                "telephone": company_telephone,
                "address": ""
                }
        }) #primero se graban los datos y luego se trae y reorganiza con formato de objeto para pasar a la vista 
        cursor = db.users.find({"company.email":company_email})
        Company = namedtuple('company', 'email name telephone address')
        User = namedtuple('User', 'email, company') #uso namedtuple para llamar los resultados como objetos con notacion con puntos, como: "company.email"
        for row in cursor:
            user = User(row['email'], Company(row['company']['email'],row['company']['name'],row['company']['telephone'],row['company']['address'])) #esta es la sintaxis necesaria para usar nametupe
        design_route = "templates/b/index.html"
        template = open(design_route).read()
        return template.format(user=user)
    
# Opcion Marketing B: Generar vista del template sin que el usuario este registrado
    @cherrypy.expose
    def unregistered(self):
        client = MongoClient()
        db = client.cherrypies
        cursor = db.users.find({"company.email":"soporte@tuempresa.cl"})
        Company = namedtuple('company', 'email name telephone address')
        User = namedtuple('User', 'email, company') #uso namedtuple para llamar los resultados como objetos con notacion con puntos, como: "company.email"
        for row in cursor:
            user = User(row['email'], Company(row['company']['name'],row['company']['email'],row['company']['telephone'],row['company']['address'])) #esta es la sintaxis necesaria para usar nametupe
        design_route = "templates/b/index.html"
        template = open(design_route).read()
        return template.format(user=user)

# Opcion Marketing C: Generar vista del template sin que el usuario este registrado
    @cherrypy.expose
    def email(self, company_name, company_email, company_telephone, company_address):
        client = MongoClient()
        db = client.cherrypies 
        result = db.users.insert_one({
            "email": "",
            "telephone": "",
            "password": "",
            "company": {
                "name": company_name,
                "email": company_email,
                "telephone": company_telephone,
                "address": company_address
                }
        }) #primero se graban los datos y luego se trae y reorganiza con formato de objeto para pasar a la vista 
        cursor = db.users.find({"company.email":company_email})
        Company = namedtuple('company', 'email name telephone address')
        User = namedtuple('User', 'email, company') #uso namedtuple para llamar los resultados como objetos con notacion con puntos, como: "company.email"
        for row in cursor:
            user = User(row['email'], Company(row['company']['email'],row['company']['name'],row['company']['telephone'],row['company']['address'])) #esta es la sintaxis necesaria para usar nametupe
        design_route = "templates/b/index.html"
        template = open(design_route).read()
        return template.format(user=user)
    

# Se pueden ver los resultados ingresando http://localhost:9090/template?design=a&email=alianzas@sigur.cl

if __name__ == '__main__':
    # Rutas y configuraciones adicionales
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd()),
        },
        '/user': {
            'tools.sessions.on': True,
        },
        '/company': {
            'tools.sessions.on': True,
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './frontend/public'
        },
        '/root': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './templates/b'
        },
        '/route': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './templates/a'
        }
    }
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.quickstart(FrontEnd(), '/', conf)
