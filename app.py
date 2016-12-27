
# -*- coding: utf-8 -*- 
import random
import string
import cherrypy
import os

class FrontEnd(object):
    @cherrypy.expose
    def index(self):
        html = open("frontend/index.html").read()
        return html

    @cherrypy.expose
    def templates(self):
	root = os.path.realpath(__file__)
        templates = open("templates/a/template.html").read()
        return templates 


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
