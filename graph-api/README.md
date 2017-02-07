get: 
* dse-driver-1.2.0-eap4.tar.gz

run: 
* mvn install:install-file -Dfile=./java-dse-graph-1.2.0-eap4.jar -DgroupId=com.datastax.cassandra -DartifactId=java-dse-graph -Dversion=1.2.0-eap4 -Dpackaging=jar
* mvn install:install-file -Dfile=./dse-driver-1.2.0-eap4.jar -DgroupId=com.datastax.cassandra -DartifactId=dse-driver -Dversion=1.2.0-eap4 -Dpackaging=jar
