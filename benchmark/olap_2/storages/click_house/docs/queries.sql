"CREATE DATABASE IF NOT EXISTS test ON CLUSTER company_cluster;

CREATE TABLE IF NOT EXISTS test.likes ON CLUSTER company_cluster (id String, user_id String, film_id String, like Int32)
ENGINE=MergeTree() ORDER BY id;"
