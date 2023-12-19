from fastapi import APIRouter, BackgroundTasks, HTTPException, Body, Depends
from typing import Annotated

from models import UserData, Tier, UserSubscription
from schema.settings import Settings
from schema.mail import EmailSchema
from schema.creatorPost import CreatorPostSchema
from config.setting import get_settings
from utils.mail import send_test

router = APIRouter(
    prefix='/HL',
    tags=['HL']
)

@router.get('/error')
async def test_error():
    raise HTTPException(
        status_code=400,
        detail='error information.'
    )

@router.get('/setting')
async def print_setting(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        'smtp_user': settings.smtp_user,
        'smtp_from': settings.smtp_from,
        'smtp_code': settings.smtp_code,
        'mssql_url_production': settings.mssql_url_production,
        'mssql_url_staging': settings.mssql_url_staging
    }

@router.post('/test_mail')
async def test_mail(background_tasks: BackgroundTasks, target: Annotated[EmailSchema, Body()]):
    background_tasks.add_task(send_test, target.email)
    return {
        'detail': {'mailStatus': 'sending'}
    }

@router.post('/createPost')
async def when_create_work(work: Annotated[CreatorPostSchema, Body(description='creatorPost')]):
    print(work.visibility)
    # 判斷方案類型 everyone? tiers?
    # SELECT (作者)所有方案-訂閱者-email
    # SELECT (作者)選擇方案-訂閱者-email
    # 背景發送email
    return {
        'detail': work.model_dump()
    }