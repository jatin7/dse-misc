# Steps to Migrate from OSS C* 3.x to DSE 5.x

## 1. Change Existing Nodes to GPFS
1. Change `cassandra-rackdc.properties` to:
  2. dc=datacenter1
  3. rack=rack1
4. Change cassandra.yaml snitch: `GossipingPropertyFileSnitch`
5. Rolling restart of nodes: `nodetool flush && nodetool drain && service cassandra stop`
6. Update application specific keyspaces to use NetworkTopology w/ only existing DC
  7. `ALTER KEYSPACE {keyspace} WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '3'}  AND durable_writes = true;`

## 2. Join DSE Nodes to Existing Cluster
1. Create new instances and install DSE 5 on all nodes, don't start dse service
2. Elect single node as DC's seed
1. Update `cassandra.yaml` to all the same settings include cluster_name etc... and optimized settings and set seed of all but on to the elected DC seed
1. On elected seed set `cassandra.yaml` seeds to 1-2 IPs in datacenter1 (existing)
2. Change `cassandra-rackdc.properties` to:
  2. dc=cassandra
  3. rack=rack1
1. Start dse service (`service dse start`) on elected DC seed node
2. Check `nodetool status` that new node joins correctly in `cassandra`
3. Start other nodes 1-by-1 w/ 2mins between each start

## 3. Add 'Cassandra' workload type for each OSS instance
DSE will make queries regularly to find out what workload type a node is (Cassandra/Search/SearchAnalytics) which if the result is `null` will fill up the logs and cause performance issues on each DSE node.  An indication this is occuring is a log message of `Couldn't determine workload for /10.10.6.255 from value NULL`.  To avoid this:
1. On each *DSE node* update the local `system.peers` table and add `Cassandra` to the workload column for each OSS node

## 4. Update Schema to include 'cassandra' or your DC name(s) in cluster:
1. Alter keyspaces to use NetworkTopStrategy: 
  2. `ALTER KEYSPACE dse_perf WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '3', 'cassandra': '3'}  AND durable_writes = true;`
  3. `ALTER KEYSPACE system_auth WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '3', 'cassandra': '3'}  AND durable_writes = true;`
  4. `ALTER KEYSPACE dse_security WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '3', 'cassandra': '3'}  AND durable_writes = true;`
  5. `ALTER KEYSPACE system_distributed WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '3', 'cassandra': '3'}  AND durable_writes = true;`
  6. `ALTER KEYSPACE dse_system WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '3', 'cassandra': '3'}  AND durable_writes = true;`
  7. `ALTER KEYSPACE dse_leases WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': '3', 'cassandra': '3'}  AND durable_writes = true;`
8. Verify that `nodetool describecluster` shows all nodes sharing the same schema ie: `Schema versions:
	d08412f3-1cba-3a9f-995d-9d97f007d329: [172.31.10.63, 172.31.10.68, 172.31.10.67, 172.31.10.66, 172.31.10.65, 172.31.10.64]`
1. Alter all remaining application specific keyspaces to be replicated in both existing and new DC
1. Rebuild each node in new DC (cassandra)  `nodetool rebuild -- datacenter1`
  2. Note: rebuild max 2-3 at a time
1. Verify that each nodes load/data looks correct by nodetool as well as cqlsh queries

## 5. Before removing nodes from old DC (datacenter1)
1. Make sure applications and spark jobs are using new DC and IPs
2. Run full repair across DCs on new DC
3. Alter all the listed keyspaces in \#3 to remove datacenter1 from the topology
  4. ie. `ALTER KEYSPACE {keyspace} WITH replication = {'class': 'NetworkTopologyStrategy', 'cassandra': '3'}  AND durable_writes = true;`
4. Use nodetool on each node to remove self from cluster `nodetool remove`
5. Verify on new DC that only those IPs exist and a single DC is shown
6. Restore `dse_leases` keyspace to EverywhereStrategy (optional: system_auth)
  7. `ALTER KEYSPACE dse_leases WITH replication = {'class': 'EverywhereStrategy'}  AND durable_writes = true;`
