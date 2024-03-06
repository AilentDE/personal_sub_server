from fastapi import APIRouter, status, HTTPException, Body, Depends, BackgroundTasks
from typing import Annotated
from dependencies.base import check_hmac
from config.database_dyanamodb import dynamodb, Key
from config.setting import setting
from schema.userData import UserData
from schema.discordOAuth import discordOauthSchema
from utils.encode_tool import encode_base64, decode_base64, hash_sha1
from utils.discord_api import exchange_token, get_discord_user_data, bot_leave_guild
from utils.jwt import encode_jws
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
        # 'scope': 'identify email',
        'scope': 'bot',
        'permissions': 8,
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
    clusters_user_data = result['Items'][0]['clustersUserData']
    if hash_sha1(clusters_user_data['email']) != signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Signature validation failed.'
        )
    
    return clusters_user_data

@router.post('/discord')
async def sign_in_discord_user(background_tasks: BackgroundTasks, discord_oauth: Annotated[discordOauthSchema, Body()]):
    # user
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
    if hash_sha1(result['Items'][0]['clustersUserData']['email']) != signature:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Signature validation failed.'
        )
    clusters_user_data = result['Items'][0]

    discord = exchange_token(discord_oauth.code)
    discord_user_data = get_discord_user_data(discord['access_token'])
    response = user_table.put_item(Item={
        'clustersUserId': f'clusters#{clusters_user_id}',
        'discordUserId': f'discord#{discord_user_data["id"]}',
        'clustersUserData': clusters_user_data,
        'discordUserData': discord_user_data
    })
    null_data = list(filter(lambda x: "#null" in x["discordUserId"], result['Items']))
    if len(null_data) !=0:
        response = user_table.delete_item(Key={
            'clustersUserId': f'clusters#{clusters_user_id}',
            'discordUserId': f'discord#{discord_user_data["id"]}'
        })
    
    # guild
    if 'guild' in discord.keys():
        guild_table = dynamodb().table('discordClusters-discordGuild')

        guild = discord['guild']
        if guild['owner_id'] != discord_user_data["id"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Must select own guild.'
            )
        result = guild_table.query(
            KeyConditionExpression=Key('guildOwner').eq(f'discord#{discord_user_data["id"]}') & Key('itemType').begins_with('guild#')
        )
        if len(result['Items']) != 0 and result['Items'][0]['itemType'] != f'guild#{guild["id"]}':
            # bot leave old guild
            background_tasks.add_task(bot_leave_guild, result['Items'][0]['itemType'].split('#')[1])
            # create new guild item
            response = guild_table.put_item(Item={
                'guildOwner': f'discord#{discord_user_data["id"]}',
                'itemType': f'guild#{guild['id']}',
                'guild': guild,
                'tierRole': {}
            })
            # delete old guild item
            response = guild_table.delete_item(Key={
                'guildOwner': f'discord#{discord_user_data["id"]}',
                'itemType': f'guild#{result["Items"][0]["itemType"]}'
            })
        elif len(result['Items']) !=0:
            # update guild item
            response = guild_table.update_item(
                Key={
                    'guildOwner': f'discord#{discord_user_data["id"]}',
                    'itemType': f'guild#{guild['id']}',
                },
                UpdateExpression='SET #guild = :guild',
                ExpressionAttributeNames={
                    '#guild': 'guild'
                },
                ExpressionAttributeValues={
                    ':guild': guild
                },
                ReturnValues='UPDATED_NEW'
            )
        else:
            # create new guild item
            response = guild_table.put_item(Item={
                'guildOwner': f'discord#{discord_user_data["id"]}',
                'itemType': f'guild#{guild['id']}',
                'guild': guild,
                'tierRole': {}
            })
    
    access_token = encode_jws({
        'primaryUserId': clusters_user_id,
        'secondaryUserId': discord_user_data['id']
    })

    return {
        'accessToken': access_token,
        'disocrdUser': discord_user_data
    }
