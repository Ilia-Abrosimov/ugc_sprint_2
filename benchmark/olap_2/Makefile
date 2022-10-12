include .env

env_file = --env-file .env

ch_file := storages/click_house/docs/queries.sql

ch_queries := $(shell cat ${ch_file})


help:
	@echo "Makefile commands:"
stop:
	docker-compose -f docker-compose.yml stop $(c)
destroy:
	docker system prune -f --volumes $(c)
launch_ch:
	docker-compose --profile ch -f docker-compose.yml build $(c)
	docker-compose --profile ch -f docker-compose.yml up -d $(c)
storages_ch:
	docker exec clickhouse-node1 clickhouse-client -n -q ${ch_queries}
launch_mongo:
	docker-compose --profile mongo -f docker-compose.yml build $(c)
	docker-compose --profile mongo -f docker-compose.yml up -d $(c)
test_click_house:
	docker-compose --profile test_click_house -f docker-compose.yml ${env_file} build $(c)
	docker-compose --profile test_click_house -f docker-compose.yml ${env_file} up -d $(c)
test_mongo:
	docker-compose --profile test_mongo -f docker-compose.yml ${env_file} build $(c)
	docker-compose --profile test_mongo -f docker-compose.yml ${env_file} up -d $(c)
