ch_node1_file := docs/queries_node1.sql
ch_node2_file := docs/queries_node2.sql
ch_node3_file := docs/queries_node3.sql
ch_node4_file := docs/queries_node4.sql

ch_node1_queries := $(shell cat ${ch_node1_file})
ch_node2_queries := $(shell cat ${ch_node2_file})
ch_node3_queries := $(shell cat ${ch_node3_file})
ch_node4_queries := $(shell cat ${ch_node4_file})

help:
	@echo "Makefile commands:"
	@echo "setup_ch"
	@echo "stop"
	@echo "restart"
	@echo "destroy"
	@echo "storages_ch"
launch_ch:
	docker-compose -f docker-compose.yml build $(c)
	docker-compose -f docker-compose.yml up -d $(c)
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

start_tests: launch_ch storages_ch
	pytest