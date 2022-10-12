"CREATE TABLE IF NOT EXISTS default.views (id Int64, user_id Int64, film_id Int64, viewed_frame Int32)
ENGINE=Distributed('company_cluster', '', views, rand());"
