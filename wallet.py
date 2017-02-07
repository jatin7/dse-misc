import time
import sys

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

#Configuration
contactpoints = ['10.0.0.252']
auth_provider = PlainTextAuthProvider (username='russ', password='DevryPOC')
keyspace = "kohls"

print "Connecting to cluster"

cluster = Cluster( contact_points=contactpoints,
                   auth_provider=auth_provider )

session = cluster.connect(keyspace)

id = 1
loop = 1
while loop == 1:
   query = "INSERT INTO wallet_by_id (id, firstName, lastName, hashedEmail, profileId, loyalityId, createdTime, updatedTime, deleted, rev) VALUES ('%d', 'Russ2', 'Katz2', 'russ@email.com', 'p12346', 'l12346', '12/30/2016', '12/30/2016', false, now());" % (id)
   session.execute(query)
   id = id + 1

cluster.shutdown()
sys.exit(0)
