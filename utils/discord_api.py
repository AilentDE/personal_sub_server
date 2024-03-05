from fastapi import HTTPException
from config.setting import setting
import urllib
import requests

base_url = 'https://discord.com/api'

def exchange_token(code: str):
    data = {
        'grant_type': 'authorization_code',
        'code': f'{code}',
        'redirect_uri': 'https://staging.clusters.tw'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post(f'{base_url}/oauth2/token', data=data, headers=headers, auth=(setting.discord_client, setting.discord_secret))
    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException(
            status_code=r.status_code,
            detail='This is an error for the OAuth code. Please try using local data or retry signing in.'
        )

def get_discord_user_data(token: str):
    headers = {
        'Authorization': 'Bearer ' + token
    }
    r = requests.get(base_url + '/users/@me', headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException(
            status_code=r.status_code,
            detail='Unable to retrieve user information.'
        )