from fastapi import APIRouter, BackgroundTasks, HTTPException, Path, Body, Depends
from fastapi.encoders import jsonable_encoder
from typing import Annotated

from models import UserData, Tier, UserSubscription
from schema.settings import Settings
from schema.mail import EmailSchema
from schema.creatorPost import CreatorPostSchema
from config.database_mssql import get_db
from config.setting import get_settings
from utils.mail import send_test, send_format_mail
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

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

@router.post('/{creator_id}/createPost')
async def when_create_work(background_tasks: BackgroundTasks, db: Annotated[Session, Depends(get_db)], creator_id: Annotated[str, Path(description='creatorId')], work: Annotated[CreatorPostSchema, Body(description='creatorPost body')]):
    print('作品類型: ', work.visibility)
    tw_datetime = datetime.utcnow() + timedelta(hours=8)
    print('現在時間: ', tw_datetime.strftime("%m-%y-%d %H:%M:%S"))

    # 作者資訊
    stmt_creator = select(UserData).where(UserData.userID == creator_id)
    result = db.execute(stmt_creator).scalar_one_or_none()
    if result:
        mail_info = {
            'creator_url': f'https://clusters.tw/profile/{result.userID}/works',
            'creator_name': result.displayName,
            'work_url': f'https://clusters.tw/creator-posts/{work.id}',
            'work_title': f'{work.title if work.title!=""else"新作品"}'
        }
        print('use', mail_info)
    else:
        raise HTTPException(
            status_code=404,
            detail='creator not fount'
        )

    # 判斷方案類型 everyone? tiers?
    match work.visibility:
        case 'everyone':
            # Saddly Pydantic can't use .join or .c without relasionship
            # '''
            # stmt = select(UserSubscription.userID, UserData.email).join(
            #     UserData, UserSubscription.userID == UserData.userID
            # ).where(
            #     UserSubscription.creatorID == creator_id,
            #     UserSubscription.subscription_Year == tw_datetime.strftime('%Y'),
            #     UserSubscription.subscription_Month == tw_datetime.strftime('%m'),
            #     UserSubscription.IsPay == True
            #     ).order_by(UserSubscription.userID.asc())
            # '''

            stmt = select(UserData).join(
                UserSubscription, UserData.userID == UserSubscription.userID
            ).where(
                UserSubscription.creatorID == creator_id,
                UserSubscription.subscription_Year == tw_datetime.strftime('%Y'),
                UserSubscription.subscription_Month == tw_datetime.strftime('%m'),
                UserSubscription.IsPay == True,
                UserSubscription.cancelUser.is_(None)
                ).order_by(UserSubscription.userID.asc())
            results = db.execute(stmt).scalars().all()
            results = list(map(lambda x: {'user_email': x.email, 'user_name': x.displayName}, results))
            results = [dict(t) for t in set([tuple(d.items()) for d in results])]
            ## 寄出email
            for tar in results:
                format_dict = mail_info.copy()
                format_dict.update(tar)
                print('to', format_dict)
                background_tasks.add_task(send_format_mail, format_dict['user_email'], '[Clusters - 可洛斯·創作者集群] {} 的新作品通知！'.format(format_dict['creator_name']), format_dict)
            return {
                'detail': {'mailStatus': 'sending'}
            }

        case 'tiers':
            # SELECT (作者)選擇方案-訂閱者-email
            if len(work.visibleTierIds) >0:
                ## 找要通知的方案
                stmt_tiers = select(Tier).where(
                    Tier.creatorID == creator_id,
                    Tier.IsDelete == False,
                    Tier.tierID.in_(work.visibleTierIds)
                ).order_by(Tier.isAddon, Tier.price)
                results = db.execute(stmt_tiers).scalars().all()
                results_normal = list(filter(lambda tier: tier.isAddon==False, results))
                results_addon = list(filter(lambda tier: tier.isAddon==True, results))
                ## 找訂閱裡有匹配方案的對象
                ### >=價格的標準方案
                if len(results_normal) > 0:
                    stmt_tier_normal = select(UserData).join(
                            UserSubscription, UserData.userID == UserSubscription.userID
                        ).where(
                        UserSubscription.creatorID == creator_id,
                        UserSubscription.subscription_Year == tw_datetime.strftime('%Y'),
                        UserSubscription.subscription_Month == tw_datetime.strftime('%m'),
                        UserSubscription.IsPay == True,
                        UserSubscription.cancelUser.is_(None),
                        UserSubscription.isAddon == False,
                        UserSubscription.price >= results_normal[0].price #only one
                    ).order_by(UserSubscription.userID.asc())
                    results_tier_normal = db.execute(stmt_tier_normal).scalars().all()
                    results_tier_normal = list(map(lambda x: {'user_email': x.email, 'user_name': x.displayName}, results_tier_normal))
                else:
                    results_tier_normal = []
                ### 等價的進階方案
                addon_list = list(map(lambda x:x.tierID, results_addon))
                if len(results_addon) > 0:
                    stmt_tier_addon = select(UserData).join(
                            UserSubscription, UserData.userID == UserSubscription.userID
                        ).where(
                        UserSubscription.creatorID == creator_id,
                        UserSubscription.subscription_Year == tw_datetime.strftime('%Y'),
                        UserSubscription.subscription_Month == tw_datetime.strftime('%m'),
                        UserSubscription.IsPay == True,
                        UserSubscription.cancelUser.is_(None),
                        UserSubscription.isAddon == True,
                        UserSubscription.tierID.in_(addon_list)
                    ).order_by(UserSubscription.userID.asc())
                    results_tier_addon = db.execute(stmt_tier_addon).scalars().all()
                    results_tier_addon = list(map(lambda x: {'user_email': x.email, 'user_name': x.displayName}, results_tier_addon))
                else:
                    results_tier_normal = []
                results = [dict(t) for t in set([tuple(d.items()) for d in (results_tier_normal+results_tier_addon)])]
                ## 寄出email
                for tar in results:
                    format_dict = mail_info.copy()
                    format_dict.update(tar)
                    print('to', format_dict)
                    background_tasks.add_task(send_format_mail, format_dict['user_email'], '[Clusters - 可洛斯·創作者集群] {} 的新作品通知！'.format(format_dict['creator_name']), format_dict)
                return {
                    'detail': {'mailStatus': 'sending'}
                }
                
        case 'self':
            return {
                'detail': {'mailStatus': 'no need'}
            }
        
        case _:
            raise HTTPException(
                status_code=400,
                detail='Not match this visibility setting'
            )