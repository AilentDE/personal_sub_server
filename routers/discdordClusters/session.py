from fastapi import APIRouter, status, HTTPException, Body, Depends
from typing import Annotated
from dependencies.base import check_hmac
from config.database_mssql import get_db
from config.database_dyanamodb import dynamodb, Key
from config.setting import setting
from schema.userData import UserData
from schema.discordOAuth import discordOauthSchema
from utils.encode_tool import encode_base64, decode_base64, hash_sha1
import urllib

router = APIRouter(
    prefix='/session',
)

@router.post('/signIn/{creator_id}')
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

@router.post('/clusters')
async def sign_in_clusters_user(discord_oauth: Annotated[discordOauthSchema, Body()]):
    user_table = dynamodb().table('discordClusters-userData')

    clusters_user_id, signature = decode_base64(discord_oauth.state).split('|')
    result = user_table.query(
        KeyConditionExpression=Key('clustersUserId').eq(f'clusters#{clusters_user_id}')
    )
    if len(result['Items']) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found.'
        )
    else:
        clusters_user_data = result['Items'][0]['clustersUserData']
        if hash_sha1(clusters_user_data['email']) != signature:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Signature validation failed.'
            )
    
    return clusters_user_data

@router.post('/discord')
async def sign_in_discord_user():
    return
