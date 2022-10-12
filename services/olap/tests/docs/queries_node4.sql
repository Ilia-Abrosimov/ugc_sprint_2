"CREATE TABLE IF NOT EXISTS default.views (id String, user_id String, film_id String, viewed_frame Int32)
ENGINE=Distributed('company_cluster', '', views, rand());"
