include .env

env_file = --env-file .env
ch_node1_file := click_house/docs/queries_node1.sql
ch_node3_file := click_house/docs/queries_node3.sql
ch_node1_queries := $(shell cat ${ch_node1_file})
ch_node3_queries := $(shell cat ${ch_node3_file})

help:
	@echo "Makefile commands:"
	@echo "setup_ch"
	@echo "stop"
	@echo "restart"
	@echo "destroy"
	@echo "storages_ch"
	@echo "test_ch_shard"
	@echo "test_ch_reg"
	@echo "test_vertica"
setup_ch:
	docker-compose --profile clickhouse -f docker-compose.yml build $(c)
	docker-compose --profile clickhouse -f docker-compose.yml up -d $(c)
setup_vertica:
	docker-compose --profile vertica -f docker-compose.yml build $(c)
	docker-compose --profile vertica -f docker-compose.yml up -d $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
destroy:
	docker system prune -a -f --volumes $(c)
storages_ch:
	docker exec clickhouse-node1 clickhouse-client -n -q ${ch_node1_queries}
	docker exec clickhouse-node3 clickhouse-client -n -q ${ch_node3_queries}
test_ch_shard:
	docker-compose --profile test_ch_shard -f docker-compose.yml ${env_file} build $(c)
	docker-compose --profile test_ch_shard -f docker-compose.yml ${env_file} up -d $(c)
test_ch_reg:
	docker-compose --profile test_ch_reg -f docker-compose.yml ${env_file} build $(c)
	docker-compose --profile test_ch_reg -f docker-compose.yml ${env_file} up -d $(c)
test_vertica:
	docker-compose --profile test_vertica -f docker-compose.yml ${env_file} build $(c)
	docker-compose --profile test_vertica -f docker-compose.yml ${env_file} up -d $(c)
