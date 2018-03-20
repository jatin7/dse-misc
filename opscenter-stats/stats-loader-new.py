#!/usr/bin/python

import sys
from random import randint

from dse.cluster import Cluster, ExecutionProfile, EXEC_PROFILE_DEFAULT
from dse.policies import DCAwareRoundRobinPolicy,TokenAwarePolicy, ConstantSpeculativeExecutionPolicy
from dse import ConsistencyLevel

#Configuration
contactpoints = ['172.31.13.134', '172.31.4.17']
localDC = "dc2"
keyspace = "stats"
CL = ConsistencyLevel.ONE
profile1 = ExecutionProfile( load_balancing_policy=DCAwareRoundRobinPolicy(local_dc=localDC, used_hosts_per_remote_dc=3),
                            speculative_execution_policy=ConstantSpeculativeExecutionPolicy(.1, 20),
                            consistency_level = CL
                            )

print "Connecting to cluster"

cluster = Cluster( contact_points=contactpoints,
                   execution_profiles={EXEC_PROFILE_DEFAULT: profile1},
                   )

session = cluster.connect(keyspace)

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
