CREATE KEYSPACE cart WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '3'}  AND durable_writes = true;

CREATE TYPE cart.accessory (
    id text,
    type text,
    productid text,
    name text,
    imageurl text,
    price text,
    quantity text,
    occasion text,
    minquantity text,
    maxquantity text
);

CREATE TYPE cart.deliveryoptions (
    method text,
    deliveryoption text,
    floristfee text,
    message text,
    fee text,
    deliverydate text,
    zipcode text,
    deliverylocation text,
    state text
);

CREATE TYPE cart.giftmessage (
    occasion text,
    message text
);

CREATE TABLE cart.ftd_cart (
    id text,
    itemid text,
    accessories frozen<accessory>,
    coupon text static,
    deliveryamount text static,
    deliveryoptions frozen<deliveryoptions>,
    description text,
    discountamount text static,
    discountpercent text static,
    email text static,
    floristamount text static,
    giftmessage frozen<giftmessage>,
    imageurl text,
    itemcount text static,
    listedprice text,
    membertype text static,
    ordernumber text static,
    productid text,
    profileid text static,
    promomessage text static,
    quantity text,
    saleprice text,
    sku text,
    sourcecode text,
    subtotalamount text static,
    subtotalprice text,
    taxamount text static,
    title text,
    totalamount text static,
    PRIMARY KEY (id, itemid)
) WITH CLUSTERING ORDER BY (itemid ASC)
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys': 'ALL', 'rows_per_partition': 'NONE'}
    AND comment = ''
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy', 'max_threshold': '32', 'min_threshold': '4'}
    AND compression = {'chunk_length_in_kb': '64', 'class': 'org.apache.cassandra.io.compress.LZ4Compressor'}
    AND crc_check_chance = 1.0
    AND dclocal_read_repair_chance = 0.1
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND nodesync = {'enabled': 'true'}
    AND read_repair_chance = 0.0
    AND speculative_retry = '99PERCENTILE';
