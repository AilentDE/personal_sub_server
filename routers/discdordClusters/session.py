from fastapi import APIRouter, status, HTTPException, Body, Depends
from typing import Annotated
from dependencies.base import check_hmac
from config.database_mssql import get_db
from config.database_dyanamodb import dynamodb, Key
from config.setting import setting
from schema.userData import UserData
from utils.encode_tool import encode_base64, hash_sha1
import urllib

router = APIRouter(
    prefix='/session',
)

@router.post('/{creator_id}/signIn')
async def request_login_url(userData: Annotated[UserData, Body()], clusters_user_id: Annotated[str, Depends(check_hmac)]):
    user_table = dynamodb().table('discordClusters-userData')

    result = user_table.query(
        KeyConditionExpression=Key('clustersUserId').eq(f'clusters#{clusters_user_id}')
    )
    discordUserId = 'discord#null' if len(result['Items']) == 0 else result['Items'][0]['discordUserId']
    response = user_table.put_item(Item={
        'clustersUserId': f'clusters#{clusters_user_id}',
        'discordUserId': discordUserId,
        'clustersUserData': userData.model_dump()
    })
    
    base_url = 'https://discord.com'
    state = encode_base64(f'{clusters_user_id}|{hash_sha1(userData.email)}')
    params = {
        'response_type': 'code',
        'client_id': setting.discord_client,
        'scope': 'identify email',
        'state': state,
        'redirect_uri': 'https://staging.clusters.tw',
        'prompt': 'consent'
    }
    encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    redirect_url = f'{base_url}/oauth2/authorize?' + encoded_params

    return {
        "success": True,
        "redirectURL": redirect_url
    }
