#!/usr/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_cors import CORS, cross_origin
import json
import uuid
import dse
import requests
from dse.cluster import Cluster
from dse.auth import DSEPlainTextAuthProvider

app = Flask(__name__)
CORS(app)

#Configuration
contactpoints = ['66.70.191.99']
auth_provider = DSEPlainTextAuthProvider (username='cassandra', password='fr0gp0w3r')
keyspace = "whois"

print "Connecting to cluster"

cluster = Cluster( contact_points=contactpoints,
                   auth_provider=auth_provider )

session = cluster.connect(keyspace)

@app.route('/')
def index():
    return "tacos and burritos"

@app.route('/incoming/info', methods=['POST'])
def info():
#   if not request.json in request.json:
#      abort(400)

   #print json.dumps(request.json)
   network = request.json['network']
   nick = request.json['nick']
   identd = request.json['identd']
   hostname = request.json['hostname']
   realname = request.json['realname']
   query = """ INSERT INTO whois.info (network, nick, identd, hostname, realname, ts) VALUES ('%s', '%s', '%s', '%s', '%s', now()); """ % (network, nick, identd, hostname, realname)
   query = """INSERT INTO whois.info_latest ( hostname, identd, network, nick, realname) VALUES ('%s','%s','%s','%s','%s' ); """ % (hostname, identd, network, nick, realname)
   print(query)
   session.execute(query)
   return "201"

@app.route('/incoming/chan', methods=['POST'])
def chan():
#   if not request.json in request.json:
#      abort(400)

   #print json.dumps(request.json)
   network = request.json['network']
   nick = request.json['nick']
   channel = request.json['channel']
   mode = request.json['mode']
   query = """ INSERT INTO whois.chan (network, nick, channel, ts, mode) VALUES ('%s', '%s', '%s', now(), '%s'); """ % (network, nick, channel, mode)
   query = """INSERT INTO whois.chan_latest ( channel, mode, network, nick) VALUES ('%s','%s','%s','%s' ); """ % (channel, mode, network, nick)
   print(query)
   session.execute(query)
   return "201"

if __name__ == '__main__':
    app.run(debug=True)
