from datetime import datetime

def write_log(message: str, log_file:str='log.txt'):
    with open('logs/' + log_file, mode='a', encoding='utf-8') as log:
        log.write(f'[{datetime.utcnow()}] ' + message)