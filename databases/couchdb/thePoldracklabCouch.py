#!/usr/bin/python

# Poldracklab CouchDB Functions
# This is the only couch we have.

import couchdb
import requests
import random

class Couch:

  """Initialize couch instance"""
  def __init__(self,server=None):
    self.server = server

  """Connect to CouchDB instance, default is localhost"""
  def connect(self):
    couch = couchdb.Server(self.server)
    

  """Insert a document into a database in the couchdb server"""
  def add_document(self,database_name,document):
    print "TODO."    

  """Sit on the couch!"""
  def sit(self): 
    import requests
    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = requests.get(word_site)
    words = response.content.splitlines()
    widx = random.randint(0,len(words)-1)
    salutations = ["My, what a %s couch.","Why does this couch smell like %s","Is that a %s under the cushion?","I've always wanted a %s couch.","Excuse me, I want some alone time with my couch, %s"]
    sidx = random.randint(0,len(salutations)-1)
    print salutations[sidx] %(words[widx])  

