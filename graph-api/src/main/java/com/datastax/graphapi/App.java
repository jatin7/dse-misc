package com.datastax.graphapi;

import com.datastax.driver.core.*;
import com.datastax.driver.dse.*;
import com.datastax.driver.dse.graph.*;

public class App {


	public static void main(String[] args) {

		DseCluster cluster;
		DseSession session;

		cluster = DseCluster.builder()
			.addContactPoint("172.31.30.38")
			.withGraphOptions(new GraphOptions().setGraphName("demo"))
			.build();
		session = cluster.connect("demo");

	GraphStatement s1 = new SimpleGraphStatement("g.addV(label, 'test_vertex')").setGraphName("demo");
	session.executeGraph(s1);

	GraphStatement s2 = new SimpleGraphStatement("g.V()").setGraphName("demo");
	GraphResultSet rs = session.executeGraph(s2);
	System.out.println(rs.one().asVertex());

		// Clean up the connection by closing it
    cluster.close();
	}
}
