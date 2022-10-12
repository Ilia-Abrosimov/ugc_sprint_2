## Тесты ClickHouse vs Mongo

### Разворачивание хранилищ
``` 
make launch_ch (Запуск контейнеров ClickHouse)
make storages_ch (Создание БД и таблиц в ClickHouse)
make launch_mongo (Запуск контейнеров Mongo)
``` 

### Запуск тестов в Docker
``` 
make test_click_house
make test_mongo
```

### Запуск тестов локально

#### ClickHouse
``` 
Файл olap_2/tests/test_click_house.py
``` 

#### Mongo
``` 
Файл olap_2/tests/test_mongo.py - требуется задать параметр local = True
``` 
