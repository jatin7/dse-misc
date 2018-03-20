#!/usr/bin/python

import sys

from dse.cluster import Cluster, ExecutionProfile
from dse.policies import DCAwareRoundRobinPolicy,TokenAwarePolicy, ConstantSpeculativeExecutionPolicy
from dse import ConsistencyLevel

from random import randint

#Configuration
contactpoints = ['172.31.0.20','172.31.11.158']
localDC = "dc2"
keyspace = "stats"
profile1 = ExecutionProfile(TokenAwarePolicy(DCAwareRoundRobinPolicy(local_dc=localDC, used_hosts_per_remote_dc=3)))
CL = ConsistencyLevel.LOCAL_QUORUM
#CL = ConsistencyLevel.LOCAL_ONE

print "Connecting to cluster"

cluster = Cluster( contact_points=contactpoints,
                   execution_profiles={"profile1": profile1}
                   )

session = cluster.connect(keyspace)
session.default_consistency_level = CL
session.retry_policy = ConstantSpeculativeExecutionPolicy( delay=0.07, max_attempts=2,)

c = 0
x = 0
while 1:

   name = randint(0,32)
   stat0 = randint(1,100)
   stat1 = randint(1,100)
   stat2 = randint(1,100)
   game = randint(1,100)
   session.execute (""" INSERT INTO stats.player_stats (name, game, ts, stat1, stat2, stat3) VALUES (%s, %s, now(), %s, %s, %s) """, (str(name), str(game), int(stat0), int(stat1), int(stat2)))
   #session.execute_async (""" INSERT INTO stats.player_stats (name, game, ts, stat1, stat2, stat3) VALUES (%s, %s, now(), %s, %s, %s) """, (str(name), str(game), int(stat0), int(stat1), int(stat2)))
   c = c + 1
   x = x + 1
   if(x == 1000):
      print(c)
      x = 0

cluster.shutdown()
sys.exit(0)
