"CREATE DATABASE IF NOT EXISTS shard;

CREATE DATABASE IF NOT EXISTS replica;

CREATE TABLE IF NOT EXISTS shard.likes (id String, user_id String, film_id String, like Int32)
Engine=ReplicatedMergeTree('/clickhouse/tables/shard1/likes', 'replica_1')
PARTITION BY film_id ORDER BY user_id;

CREATE TABLE IF NOT EXISTS replica.likes (id String, user_id String, film_id String, like Int32)
Engine=ReplicatedMergeTree('/clickhouse/tables/shard2/likes', 'replica_2')
PARTITION BY film_id ORDER BY user_id;

CREATE TABLE IF NOT EXISTS default.views (id String, user_id String, film_id String, viewed_frame Int32)
ENGINE=Distributed('company_cluster', '', views, rand());

CREATE TABLE IF NOT EXISTS default.likes (id String, user_id String, film_id String, like Int32)
ENGINE=Distributed('company_cluster', '', likes, rand());"
