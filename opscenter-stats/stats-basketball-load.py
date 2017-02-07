#!/usr/bin/python

import time
import sys

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

from random import randint

#Configuration
contactpoints = ['54.152.60.220','52.87.197.72']
auth_provider = PlainTextAuthProvider (username='russ', password='StatsDemo')
keyspace = "stats"

print "Connecting to cluster"

startTime = time.time()
cluster = Cluster( contact_points=contactpoints,
                   auth_provider=auth_provider )

session = cluster.connect(keyspace)

while 1:
   
   name = randint(0,32)
   stat0 = randint(1,100)
   stat1 = randint(1,100)
   stat2 = randint(1,100)
   game = randint(1,100)
   #session.execute (""" INSERT INTO stats.player_stats (name, game, ts, stat1, stat2, stat3) VALUES (%s, %s, now(), %s, %s, %s) """, (str(name), str(game), int(stat0), int(stat1), int(stat2)))
   session.execute_async (""" INSERT INTO stats.player_stats (name, game, ts, stat1, stat2, stat3) VALUES (%s, %s, now(), %s, %s, %s) """, (str(name), str(game), int(stat0), int(stat1), int(stat2)))

cluster.shutdown()
sys.exit(0)
