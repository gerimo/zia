# -*- coding: utf-8 -*- 
# Estamos usando un sevidor HTTP que viene incluido en el framwork de Cherrypy
# Usamos como base de datos MONGODB. La base de datos se llama "cherrypies".
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
    name = "TusWebs.cl"
    telephone = "22 938 1010"
    address = "La Concepcion 81"
    commune = "Providencia"
    city = "Santiago"
    country = "Chile"
    js = """var parallax_map;
        $().ready(function(){
            responsive = $(window).width();
        
            examples.initContactUsMap();
            
            if (responsive >= 768){
                parallax_map = $('.parallax').find('.big-map');
                
                $(window).on('scroll',function(){           
                    parallax();
                    gsdk.checkScrollForTransparentNavbar();
                });
            }
            
        });        

       var parallax = function() {
            var current_scroll = $(this).scrollTop();
            
            oVal = ($(window).scrollTop() / 3); 
            parallax_map.css('top',oVal);
        };"""

# Vistas basicas 
    @cherrypy.expose
    def index(self):
        header = open('frontend/views/header.html').read()
        nav = open('frontend/views/nav.html').read() 
        body = open('frontend/index.html').read()
        footer = open('frontend/views/footer.html').read()
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
                "address": "Tu Direccion Comercial 100",
                "webpage": {
                    "title_1": "Estudio Contable Profesional en Santiago de Chile",
                    "tag_line_1":"",
                    "menu_1":"Inicio",
                    "menu_2":"Propuesta y servicios",
                    "menu_3":"Clientes",
                    "menu_4":"Contacto",
                    "summary_title_1":"Nuestra Propuesta",
                    "summary_content_1":"El objetivo de su empresa es maximizar los retornos para sus accionistas. Trabajamos para ayudarle a conseguirlo.",
                    "proposition_title_1": "Servicios contables",
                    "proposition_title_2": "Asesoría y planificación tributaria",
                    "proposition_title_3": "Auditoría",
                    "proposition_title_4": "Servicios financieros",
                    "proposition_content_1": "Declaración mensual de impuestos",
                    "proposition_content_2": "Planificamos sus tributaciones para disminuir el pago de rentas",
                    "proposition_content_3": "Auditoria de sus Estados Financieros",
                    "proposition_content_4": "Asesoramiento en la presentación de proyectos frente a inversionistas",
                    "service_title_1":"Nuestros servicios",
                    "service_subtitle_1":"Distintos servicios standard",
                    "pricing_title_1":"Estándard",
                    "pricing_title_2":"Contable, impositivo y legal",
                    "pricing_title_3":"Servicios Específicos",
                    "pricing_content_1":"Estándard1",
                    "pricing_content_2":"Estándard2",
                    "pricing_content_3":"Estándard3",
                    "pricing_content_4":"Estándard4",
                    "pricing_content_5":"Estándard5",
                    "pricing_content_6":"Estándard6",
                    "customer_title_1":"Lo que nuestros clientes dicen",
                    "customer_subtitle_1":"Lo que nuestros clientes dicen",
                    "customer_content_1":"Lo que nuestros clientes dicen",
                    "customer_content_2":"Lo que nuestros clientes dicen",
                    "customer_content_3":"Lo que nuestros clientes dicen",  
                    "about_title_1:": "Sobre Nosotros",
                    "about_content_1": "Estudio contable con años de experiencia asesorando tributariamente a nuestros clientes",
                    "contact_title_1":"Contáctanos",
                    "contact_content_1":"Escribenos para agendar una reunión y comprender más nuestros servicio",
                    "action":"Ver más"
                    }
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
        User = namedtuple('User', 'email telephone, company') #uso namedtuple para llamar los resultados como objetos con notacion con puntos, como: "company.email"
        Company = namedtuple('company', 'email name telephone address')
#        Webpage = namedtuple('webpage', )
        for row in cursor:
            user = User(row['email'], Company(row['company']['email'],row['company']['name'],row['company']['telephone'],row['company']['address'])) #esta es la sintaxis necesaria para usar nametupe
        design_route = "templates/b/index.html"
        template = open(design_route).read()
        return template.format(user=user)
    
# Opcion Marketing B: Generar vista del template sin que el usuario este registrado
    @cherrypy.expose
    def example_create(self):
        client = MongoClient()
        db = client.cherrypies        
        result = db.users.insert_one(
        {
            "email": "email@email.com",
            "telephone": "22 200 2000",
            "password": "",
            "company": {
                "name": "Tu Empresa",
                "email": "prueba@tuempresa.cl",
                "telephone": "22 200 2000",
                "address": "Tu Direccion Comercial 100",
                "webpage": {
                    "title": "Estudio Contable Profesional en Santiago de Chile"
                           }
                        }    
        }) 
        return "Objeto creado"

# Opcion Marketing B: Generar vista del template sin que el usuario este registrado
    @cherrypy.expose
    def example_view(self):
        client = MongoClient()
        db = client.cherrypies
        cursor = db.users.find({"company.email":"prueba@tuempresa.cl"})
        User = namedtuple('User', 'email telephone, company') #uso namedtuple para llamar los resultados como objetos con notacion con puntos, como: "company.email"
        Company = namedtuple('company', 'email name telephone address, webpage')
        Webpage = namedtuple('webpage', 'title') 
        for row in cursor:
            user = User(row['email'],row['telephone'], Company(row['company']['email'],row['company']['name'],row['company']['telephone'],row['company']['address'],Webpage(row['company']['webpage']['title']))) #esta es la sintaxis necesaria para usar nametupe
        design_route = "templates/a/1.html"
        template = open(design_route).read()
        return template.format(user=user, our=FrontEnd)

    @cherrypy.expose
    def unregistered(self):
        client = MongoClient()
        db = client.cherrypies
        cursor = db.users.find({"company.email":"soporte@tuempresa.cl"})
        User = namedtuple('User', 'email, company') #uso namedtuple para llamar los resultados como objetos con notacion con puntos, como: "company.email"
        Company = namedtuple('company', 'email name telephone address')
        Webpage = namedtuple('webpage', 'title') 
        for row in cursor:
            user = User(row['email'], Company(row['company']['email'],row['company']['name'],row['company']['telephone'],row['company']['address'])) #esta es la sintaxis necesaria para usar nametupe
        design_route = "templates/a/index.html"
        template = open(design_route).read()
        return template.format(user=user, our=FrontEnd)

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
        design_route = "templates/a/index.html"
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
            'tools.staticdir.dir': './templates/a'
        }
    }
    cherrypy.config.update({'server.socket_port': 9090})
    cherrypy.quickstart(FrontEnd(), '/', conf)
