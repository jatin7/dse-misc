#!/usr/bin/python

import time
import sys

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import DCAwareRoundRobinPolicy
from cassandra import ConsistencyLevel
from random import randint

#Configuration
contactpoints = ['172.31.14.14','172.31.11.194']
auth_provider = PlainTextAuthProvider (username='russ', password='StatsDemo')
keyspace = "poctest"
localDC = "dc1"
delay = 1
CL = ConsistencyLevel.LOCAL_QUORUM
#CL = ConsistencyLevel.LOCAL_ONE

print "Connecting to cluster"

cluster = Cluster( contact_points=contactpoints,
                   load_balancing_policy=DCAwareRoundRobinPolicy(local_dc=localDC, used_hosts_per_remote_dc=3),
                   auth_provider=auth_provider )

session = cluster.connect()
session.default_consistency_level = CL

session.execute("CREATE KEYSPACE IF NOT EXISTS poctest WITH replication = {'class' : 'NetworkTopologyStrategy', 'dc1' : 3, 'dc2' : 3};")
session.execute("CREATE TABLE IF NOT EXISTS poctest.test (id text PRIMARY KEY, c0 int, c1 int, c2 int, t0 text)")
session.execute("TRUNCATE poctest.test")

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
