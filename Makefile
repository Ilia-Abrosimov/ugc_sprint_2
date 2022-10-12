include .env

env_file = --env-file .env

ch_node1_file := services/olap/docs/queries_node1.sql
ch_node2_file := services/olap/docs/queries_node2.sql
ch_node3_file := services/olap/docs/queries_node3.sql
ch_node4_file := services/olap/docs/queries_node4.sql

ch_node1_queries := $(shell cat ${ch_node1_file})
ch_node2_queries := $(shell cat ${ch_node2_file})
ch_node3_queries := $(shell cat ${ch_node3_file})
ch_node4_queries := $(shell cat ${ch_node4_file})

help:
	@echo "Makefile commands:"
	@echo "launch_oltp"
	@echo "launch_ch"
	@echo "launch_olap"
	@echo "launch_etl"
	@echo "stop"
	@echo "restart"
	@echo "destroy"
	@echo "storages_ch"
	@echo "storages_ch_2"
	@echo "mongo"
	@echo "mongo_set"
	@echo "mongo_db"
	@echo "mongo_drop_db"
launch_oltp:
	docker-compose --profile oltp -f docker-compose.yml build $(c)
	docker-compose --profile oltp -f docker-compose.yml up $(c)
launch_ch:
	docker-compose --profile ch -f docker-compose.yml build $(c)
	docker-compose --profile ch -f docker-compose.yml up -d $(c)
launch_olap:
	docker-compose --profile olap -f docker-compose.yml build $(c)
	docker-compose --profile olap -f docker-compose.yml up -d $(c)
launch_etl:
	docker-compose --profile etl -f docker-compose.yml build $(c)
	docker-compose --profile etl -f docker-compose.yml up -d $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
destroy:
	docker system prune -a -f --volumes $(c)
storages_ch:
	docker exec clickhouse-node1 clickhouse-client -n -q ${ch_node1_queries}
	docker exec clickhouse-node2 clickhouse-client -n -q ${ch_node2_queries}
	docker exec clickhouse-node3 clickhouse-client -n -q ${ch_node3_queries}
	docker exec clickhouse-node4 clickhouse-client -n -q ${ch_node4_queries}
storages_ch_2:
	docker exec clickhouse-node1 clickhouse-client -n -q ${ch_node1_queries}
	docker exec clickhouse-node3 clickhouse-client -n -q ${ch_node3_queries}
mongo:
	docker-compose --profile mongo -f docker-compose.yml build $(c)
	docker-compose --profile mongo -f docker-compose.yml up -d $(c)
mongo_set:
	docker exec -it mongocfg1 bash -c 'echo "rs.initiate({_id: \"mongors1conf\", configsvr: true, members: [{_id: 0, host: \"mongocfg1\"}, {_id: 1, host: \"mongocfg2\"}, {_id: 2, host: \"mongocfg3\"}]})" | mongosh'
	docker exec -it mongors1n1 bash -c 'echo "rs.initiate({_id: \"mongors1\", members: [{_id: 0, host: \"mongors1n1\"}, {_id: 1, host: \"mongors1n2\"}, {_id: 2, host: \"mongors1n3\"}]})" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors1/mongors1n1\")" | mongosh'
	docker exec -it mongors2n1 bash -c 'echo "rs.initiate({_id: \"mongors2\", members: [{_id: 0, host: \"mongors2n1\"}, {_id: 1, host: \"mongors2n2\"}, {_id: 2, host: \"mongors2n3\"}]})" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.addShard(\"mongors2/mongors2n1\")" | mongosh'
mongo_db:
	docker exec -it mongors1n1 bash -c 'echo "use $(MONGO_DB)" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.enableSharding(\"$(MONGO_DB)\")" | mongosh'

	docker exec -it mongos1 bash -c 'echo "db.createCollection(\"$(MONGO_DB).likes\")" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"$(MONGO_DB).likes\", {\"user_id\": \"hashed\"})" | mongosh'

	docker exec -it mongos1 bash -c 'echo "db.createCollection(\"$(MONGO_DB).reviews\")" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"$(MONGO_DB).reviews\", {\"user_id\": \"hashed\"})" | mongosh'

	docker exec -it mongos1 bash -c 'echo "db.createCollection(\"$(MONGO_DB).bookmarks\")" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"$(MONGO_DB).bookmarks\", {\"user_id\": \"hashed\"})" | mongosh'

	docker exec -it mongos1 bash -c 'echo "db.createCollection(\"$(MONGO_DB).review_likes\")" | mongosh'
	docker exec -it mongos1 bash -c 'echo "sh.shardCollection(\"$(MONGO_DB).review_likes\", {\"user_id\": \"hashed\"})" | mongosh'
mongo_drop_db:
	docker exec -it mongos1 bash -c "mongosh $(MONGO_DB) --eval 'db.dropDatabase()'"
	docker exec -it mongos2 bash -c "mongosh $(MONGO_DB) --eval 'db.dropDatabase()'"
