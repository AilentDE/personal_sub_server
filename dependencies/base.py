from fastapi import HTTPException, Path, Header
import hmac
from hashlib import sha1
from datetime import datetime, timedelta
from config.setting import setting

def get_template(template_file:str='templates/sample_template.txt')->str:
    with open(template_file, 'r', encoding='utf-8') as template:
        body = template.read()
    return body

def write_log(message: str, log_file:str='log.txt'):
    with open('logs/' + log_file, mode='a', encoding='utf-8') as log:
        log.write(f"[{datetime.utcnow()}] " + message)

def check_hmac(
        creator_id: str = Path(..., description="creator_id from path"),
        x_iso_string: str = Header(..., description="request ISOString"),
        x_signature: str = Header(..., description="Signature from header")
        ):
    key = setting.hmac_key
    code = creator_id+'|'+x_iso_string
    hmac_code = hmac.new(key.encode(), code.encode(), sha1).hexdigest()
    if hmac_code != x_signature:
        raise HTTPException(
            status_code=401,
            detail='validation failed.'
        )
    request_datetime = datetime.strptime(x_iso_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    now_datetime = datetime.utcnow()
    if (now_datetime - request_datetime) > timedelta(minutes=5):
        raise HTTPException(
            status_code=401,
            detail='timeout.'
        )
    return creator_id