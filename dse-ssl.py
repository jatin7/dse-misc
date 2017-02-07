import time
import sys

from prettytable import PrettyTable

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import ssl


#Configuration
contactpoints = ['10.240.0.2']
ssl_opts = {'ca_certs': '/tmp/node0.key.pem',
            'ssl_version': ssl.PROTOCOL_TLSv1}

keyspace = "test"
query = "SELECT * FROM test.table1"

print "Connecting to cluster"

startTime = time.time()
cluster = Cluster( contact_points=contactpoints,
                   ssl_options=ssl_opts )

session = cluster.connect(keyspace)

print "Seconds to connect to cluster: ", time.time() - startTime

startTime = time.time()
result = session.execute(query)[:]

print "Seconds to run query: ", time.time() - startTime

output = PrettyTable(["id"])

for i in result:
 output.add_row([i[0]])

print output

cluster.shutdown()
sys.exit(0)
