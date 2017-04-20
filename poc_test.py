#!/usr/bin/python

import time
import sys

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from random import randint

#Configuration
contactpoints = ['127.0.0.1','127.0.0.1']
auth_provider = PlainTextAuthProvider (username='russ', password='StatsDemo')
keyspace = "poctest"
delay = 1 

print "Connecting to cluster"

cluster = Cluster( contact_points=contactpoints,
                   auth_provider=auth_provider )

session = cluster.connect()

#session.execute("CREATE KEYSPACE IF NOT EXISTS poctest WITH replication = {'class' : 'NetworkTopologyStrategy', 'dc1' : 3, 'dc2' : 3};")
session.execute("CREATE KEYSPACE IF NOT EXISTS poctest WITH replication = {'class' : 'SimpleStrategy', 'replication_factor': 1 };")
time.sleep(3)
session.execute("CREATE TABLE IF NOT EXISTS poctest.test (id text PRIMARY KEY, c0 int, c1 int, c2 int, t0 text)")

keys = []
loop = 0
while 1:
   loop += 1
   id = randint(1,32000)
   c0 = randint(1,100)
   c1 = randint(1,100)
   c2 = randint(1,100)
   keys.append(id)
   print "Inserting: ", id, c0, c1, c2, "first" 
   session.execute (""" INSERT INTO poctest.test (id, c0, c1, c2, t0) VALUES ('%s', %s, %s, %s, 'first') """ % (str(id), int(c0), int(c1), int(c2)))
   time.sleep(delay)
   print "Updating: ", id, c0, c1, c2, "updated" 
   session.execute (""" INSERT INTO poctest.test (id, c0, c1, c2, t0) VALUES ('%s', %s, %s, %s, 'updated') """ % (str(id), int(c0), int(c1), int(c2)))
   time.sleep(delay)
   row = session.execute(""" SELECT * FROM poctest.test WHERE id = '%s' """ % id)[:]
   print "Selected: " , (row[0])
   time.sleep(delay)
   if(loop == 5):
      for k in keys:
         print "Deleting: ", k
         session.execute(""" DELETE FROM poctest.test WHERE id = '%s' """ % k)
      keys = []
      loop = 0
         

cluster.shutdown()
sys.exit(0)
