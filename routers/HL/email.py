from fastapi import APIRouter, BackgroundTasks, HTTPException, Body
from typing import Annotated

from ...utils.mail import send_notification

router = APIRouter(
    prefix='/HL',
    tags=['HL']
)

@router.get('/test')
async def test_api():
    return {
        'detail': 'hi mail.'
    }

@router.get('/error')
async def test_error():
    raise HTTPException(
        status_code=400,
        detail='error information.'
    )

# 避免未來結構變更直接用dict接收body
@router.post('/createPost')
async def when_create_work(work: Annotated[dict, Body(description='creatorPost')]):
    print(work)
    # 判斷方案類型 everyone? tiers?
    # SELECT 作者-所有方案-訂閱者-email
    # SELECT 作者-選擇方案-訂閱者-email
    # 背景發送email
    return {
        'detail': work
    }