from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from config.setting import setting

def encode_jws(data:dict, expire_delta_hours:int=0):
    # token expire time
    if expire_delta_hours != 0:
        expire = datetime.now(tz=timezone.utc) + timedelta(hours=expire_delta_hours)
        exp = int(expire.timestamp())
        data.update({
            'exp': exp
        })
        
    data.update({
        'createdAt': datetime.now(tz=timezone.utc).isoformat().replace('+00:00', 'Z')
    })
    encoded_jws = jwt.encode(
        data,
        setting.secret_key,
        algorithm=setting.algorithm
    )
    return encoded_jws

def decode_jws(token:str):
    try:
        payload = jwt.decode(
            token,
            setting.secret_key,
            algorithms=[setting.algorithm],
            # options={"verify_exp": True, "leeway": 10}
        )
        return payload
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials.',
            headers={"WWW-Authenticate": "Bearer"},
        )