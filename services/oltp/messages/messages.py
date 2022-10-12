def message(key, variable_1=False, variable_2=False):
    messages = {
        'send_kafka': f'Message by user_id = {variable_1} send to kafka'
    }
    return messages.get(key)


class Errors:
    NOT_EXISTS = 'Not exist.'
    ALREADY_EXISTS = 'Already exists.'
