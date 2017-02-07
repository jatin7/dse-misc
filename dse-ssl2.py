import time
import sys

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.policies import (RoundRobinPolicy, SimpleConvictionPolicy,
                                ExponentialReconnectionPolicy, HostDistance,
                                RetryPolicy)
from cassandra.policies import (RoundRobinPolicy, DCAwareRoundRobinPolicy,
                                TokenAwarePolicy, SimpleConvictionPolicy,
                                HostDistance, ExponentialReconnectionPolicy,
                                RetryPolicy, WriteType,
                                DowngradingConsistencyRetryPolicy, ConstantReconnectionPolicy,
                                LoadBalancingPolicy, ConvictionPolicy, ReconnectionPolicy, FallthroughRetryPolicy)
import ssl


#Configuration
abs_path_server_keystore_path = '/usr/share/dse/conf/node0.cer'
DEFAULT_PASSWORD = 'cassandra'

contactpoints = ['104.198.206.15']
abs_path_ca_cert_path = '/tmp/ca.certs'
abs_driver_keyfile = '/usr/share/dse/conf/node0.key.pem'
abs_driver_certfile = '/usr/share/dse/conf/node0.cer.pem'
ssl_opts = {'ca_certs': abs_path_ca_cert_path,
               'ssl_version': ssl.PROTOCOL_TLSv1,
               'keyfile': abs_driver_keyfile,
               'certfile': abs_driver_certfile}

keyspace = "test"
query = "SELECT * FROM test.table1"

print "Connecting to cluster"

startTime = time.time()
#cluster = Cluster( contact_points=contactpoints,
#                   ssl_options=ssl_opts )

cluster = Cluster(
        contact_points=contactpoints,
        load_balancing_policy=TokenAwarePolicy(DCAwareRoundRobinPolicy(local_dc='dc1')),
        ssl_options=ssl_opts,
        default_retry_policy = RetryPolicy()
         )

session = cluster.connect(keyspace)

print "Seconds to connect to cluster: ", time.time() - startTime

startTime = time.time()
result = session.execute(query)[:]

print "Seconds to run query: ", time.time() - startTime

print result

cluster.shutdown()
sys.exit(0)
