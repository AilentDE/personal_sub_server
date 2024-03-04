import base64
from hashlib import sha1

def encode_base64(input_string: str):
    encoded_bytes = base64.b64encode(input_string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string

def decode_base64(input_string: str):
    decoded_bytes = base64.b64decode(input_string)
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string

def hash_sha1(input_string: str):
    sha1_hash = sha1(input_string.encode()).hexdigest()
    return sha1_hash