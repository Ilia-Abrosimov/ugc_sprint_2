"CREATE DATABASE IF NOT EXISTS shard;

CREATE DATABASE IF NOT EXISTS replica;

CREATE TABLE IF NOT EXISTS shard.views (id Int64, user_id Int64, film_id Int64, viewed_frame Int32)
Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/views', 'replica_1')
PARTITION BY film_id ORDER BY user_id;

CREATE TABLE IF NOT EXISTS replica.views (id Int64, user_id Int64, film_id Int64, viewed_frame Int32)
Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/views', 'replica_2')
PARTITION BY film_id ORDER BY user_id;

CREATE TABLE IF NOT EXISTS default.views (id Int64, user_id Int64, film_id Int64, viewed_frame Int32)
ENGINE = Distributed('company_cluster', '', views, rand());"
