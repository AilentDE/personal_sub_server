from fastapi import APIRouter, status, HTTPException, Depends, Body
from typing import Annotated
from dependencies.oauth import oauth_check
from config.database_dyanamodb import dynamodb, Key
from config.database_mssql import get_db
from config.setting import setting
from utils.encode_tool import encode_base64, hash_sha1
# from schema.tierRole import TierRoleSchema
from models.tiers import Tier
from sqlalchemy import select
from sqlalchemy.orm import Session
import urllib

router = APIRouter(
    prefix='/discord'
)

@router.get('/tierRole')
async def get_tier_role_table(db: Annotated[Session, Depends(get_db)], user_payload: Annotated[dict, Depends(oauth_check)]):
    guild_table = dynamodb().table(setting.dynamodb_table_guild)
    result_guild = guild_table.query(
        KeyConditionExpression=Key('guildOwner').eq(f"discord#{user_payload['secondaryUserId']}") & Key('itemType').begins_with('guild#')
    )

    user_table = dynamodb().table(setting.dynamodb_table_user)
    result_user = user_table.query(
        KeyConditionExpression = Key('accountType').eq(f"clusters#{user_payload['primaryUserId']}"),
    )
    user_data = result_user['Items'][0]

    base_url = 'https://discord.com'
    state = encode_base64(f"{user_payload['primaryUserId']}|{hash_sha1(user_data['email'])}")
    params = {
        'response_type': 'code',
        'client_id': setting.discord_client,
        'scope': 'bot',
        'permissions': 8,
        'state': state,
        'redirect_uri': setting.discord_redirect_uri,
        'prompt': 'consent'
    }
    encoded_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    redirect_url = f"{base_url}/oauth2/authorize?" + encoded_params
    
    if len(result_guild['Items']) == 0:
        return {
            "redirectURL": redirect_url,
            "message": "未綁定discord伺服器，請至授權頁進行綁定。",
            "tiers": [],
            "guild": {},
            "tierRole": {}
        }
    else:
        # 處理非主clusters帳號綁discord guild
        if user_payload['primaryUserId'] not in result_guild['Items'][0]['clustersUserIds']:
            response = guild_table.update_item(
                Key={
                    'guildOwner': result_guild['Items'][0]['guildOwner'],
                    'itemType': result_guild['Items'][0]['itemType'],
                },
                UpdateExpression='SET #clustersUserIds = :clustersUserIds',
                ExpressionAttributeNames={
                    '#clustersUserIds': 'clustersUserIds'
                },
                ExpressionAttributeValues={
                    ':clustersUserIds': [*result_guild['Items'][0]['clustersUserIds'], user_payload['primaryUserId']]
                },
                ReturnValues='UPDATED_NEW'
            )
        
        stmt = select(Tier).where(
            Tier.creatorID == user_payload['primaryUserId'],
            Tier.IsDelete == False
        ).order_by(
            Tier.isAddon.asc(),
            Tier.price.asc()
        )
        result_tier = db.execute(stmt).scalars().all()
        return {
            "redirectURL": redirect_url,
            "message": "成功取得discord伺服器資料",
            "tiers": result_tier,
            "guild": result_guild['Items'][0]['guild'],
            "tierRole": result_guild['Items'][0]['tierRole']
        }
    
@router.put('/tierRole')
async def update_tier_role(user_payload: Annotated[dict, Depends(oauth_check)], tierRole: Annotated[dict, Body()]):
    guild_table = dynamodb().table(setting.dynamodb_table_guild)
    result_guild = guild_table.query(
        KeyConditionExpression=Key('guildOwner').eq(f"discord#{user_payload['secondaryUserId']}") & Key('itemType').begins_with('guild#')
    )
    if len(result_guild['Items']) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No binding guild.'
        )
    else:
        guild = result_guild['Items'][0]['guild']

    response = guild_table.update_item(
        Key={
            'guildOwner': f"discord#{user_payload['secondaryUserId']}",
            'itemType': f"guild#{guild['id']}"
        },
        UpdateExpression='SET #tierRole = :tierRole',
        ExpressionAttributeNames={
            '#tierRole': 'tierRole'
        },
        ExpressionAttributeValues={
            ':tierRole': tierRole
        },
        ReturnValues='UPDATED_NEW'
    )
    return {
        "message": "成功更新discord伺服器身分組設定",
        "tierRole": tierRole
    }