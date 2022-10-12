"""

Управляющий файл ETL-системы.

Из хранилища пользовательских данных информация собирается со всех топиков, так как
в перспективе для загрузки в аналитические БД могут потребоваться данные из нескольких
топиков одновременно.

"""
import time

from src.components.extractor.extractor import KafkaExtractor
from src.components.loader.ch_loader import ClickHouseLoader
from src.components.transformer.ch_transformer import ClickHouseTransformer
from src.core.settings import etl_settings

if __name__ == '__main__':
    extractor = KafkaExtractor()
    ch_transformer = ClickHouseTransformer()
    ch_loader = ClickHouseLoader()

    records = extractor.consume()

    while True:
        try:
            record = next(records)
        except StopIteration:
            time.sleep(etl_settings.etl_manager_timeout)
        else:
            if record:
                ch_data_dict = ch_transformer.transform(record)
                ch_loader.upload_data(ch_data_dict)
                extractor.commit()
            else:
                time.sleep(etl_settings.etl_manager_timeout)
