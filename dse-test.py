import time
import sys

from prettytable import PrettyTable

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

#Configuration
contactpoints = ['54.159.232.149','54.209.96.0']
auth_provider = PlainTextAuthProvider (username='russ', password='DevryPOC')
keyspace = "test"
query = "SELECT * FROM test.table1"

print "Connecting to cluster"

startTime = time.time()
cluster = Cluster( contact_points=contactpoints,
                   auth_provider=auth_provider )

session = cluster.connect(keyspace)

print "Seconds to connect to cluster: ", time.time() - startTime

startTime = time.time()
result = session.execute(query)[:]

print "Seconds to run query: ", time.time() - startTime

output = PrettyTable(["beacon", "date", "readtime", "data"])

for i in result:
 output.add_row([i[0], i[1], i[2], i[3]])

print output

cluster.shutdown()
sys.exit(0)
