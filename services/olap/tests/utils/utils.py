import json
import random
from uuid import uuid4


def create_data_json(data_file: str = 'src.json'):
    data = []
    k = 0
    for i in range(20):
        film_id = str(uuid4())
        for j in range(random.randint(1, 10)):
            k += 1
            data.append([k, str(uuid4()), film_id, random.randint(0, 100)])
    with open(data_file, 'w') as f:
        json.dump(data, f)


if __name__ == '__main__':
    create_data_json()
