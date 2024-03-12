from fastapi import HTTPException
from config.setting import setting
import urllib
import requests

base_url = 'https://discord.com/api'

def exchange_token(code: str):
    data = {
        'grant_type': 'authorization_code',
        'code': f"{code}",
        'redirect_uri': setting.discord_redirect_uri
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    r = requests.post(f"{base_url}/oauth2/token", data=data, headers=headers, auth=(setting.discord_client, setting.discord_secret))
    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException(
            status_code=r.status_code,
            detail=f"This is an error for the OAuth code. Please try using local data or retry signing in. - {r.text}"
        )

def get_discord_user_data(access_token: str):
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    r = requests.get(base_url + '/users/@me', headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        raise HTTPException(
            status_code=r.status_code,
            detail='Unable to retrieve user information.'
        )

def bot_leave_guild(guild_id: str):
    headers = {
        'Authorization': f"Bot {setting.bot_token}"
    }
    response = requests.delete(base_url + f"/users/@me/guilds/{guild_id}", headers=headers)
    return