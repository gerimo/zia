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

import cherrypy
class index(object):
	@cherrypy.expose
	def example(self):
		var = "hello"
		index = open("index.html").read()
		return index
