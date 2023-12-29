from fastapi import APIRouter, BackgroundTasks, HTTPException, Body, Depends, Path
from typing import Annotated
from models import UserData, Tier, UserSubscription, FileList
from schema.mail import EmailSchema
from schema.creatorPost import CreatorPostSchema
from config.database_mssql import get_db
from dependencies.base import check_hmac
from utils.mail import send_test_ses, send_format_mail_ses
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import pytz

router = APIRouter(
    prefix='/email',
    tags=['email']
)

@router.post('/testMail')
async def test_mail(background_tasks: BackgroundTasks, target: Annotated[EmailSchema, Body()]):
    background_tasks.add_task(send_test_ses, target.email)
    return {
        'detail': {'mailStatus': 'sending'}
    }

@router.post('/{creator_id}/createPost')
async def when_create_work(background_tasks: BackgroundTasks, db: Annotated[Session, Depends(get_db)], creator_id: Annotated[str, Depends(check_hmac)], work: Annotated[CreatorPostSchema, Body(description='creatorPost body')]):
    print('作品類型: ', work.visibility)
    tw_datetime = datetime.utcnow() + timedelta(hours=8)
    print('現在時間: ', tw_datetime.strftime("%m-%y-%d %H:%M:%S"))

    # 作者資訊&作品資訊
    stmt_creator = select(UserData).where(UserData.userID == creator_id)
    result = db.execute(stmt_creator).scalar_one_or_none()
    if result:
        mail_info = {
            'creator_url': f'https://clusters.tw/profile/{result.userID}/works',
            'creator_name': result.displayName,
            'work_url': f'https://clusters.tw/creator-posts/{work.id}',
            'work_title': f'{work.title if work.title else "新作品"}',
            'work_excerpt': f'{work.excerpt}',
            'thumbnail_object': None,
            'thumbnail_URL': 'https://clusters-open-assets.s3.ap-northeast-1.amazonaws.com/default-work-cover.jpg'
        }
        print('use', mail_info)
    else:
        raise HTTPException(
            status_code=404,
            detail='creator not fount'
        )
    
    ## 取得封面資源
    if work.thumbnailAssetId:
        stmt = select(FileList).where(FileList.fileID == work.thumbnailAssetId)
        result = db.execute(stmt).scalar_one_or_none()
        if result:
            mail_info['thumbnail_object'] = result.filePath + result.fileName
    
    work_datetime = work.publishedAt
    now_datetime = datetime.now(tz=pytz.UTC)
    # 判斷方案類型 everyone? tiers?
    # 未來文章不做通知
    if (work.visibility in ['everyone', 'tiers']) and (now_datetime > work_datetime):
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

        ## 取得通知名單
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
            background_tasks.add_task(send_format_mail_ses, format_dict['user_email'], '【Clusters - 可洛斯·創作者集群】{} 的新作品 {}'.format(format_dict['creator_name'], format_dict['work_title']), format_dict)
        return {
            'detail': {'mailStatus': 'sending'}
        }

        # // 先取消tiers的針對信件，採取全發信。
        #  case 'tiers':
        #     # SELECT (作者)選擇方案-訂閱者-email
        #     if len(work.visibleTierIds) >0:
        #         ## 找要通知的方案
        #         stmt_tiers = select(Tier).where(
        #             Tier.creatorID == creator_id,
        #             Tier.IsDelete == False,
        #             Tier.tierID.in_(work.visibleTierIds)
        #         ).order_by(Tier.isAddon, Tier.price)
        #         results = db.execute(stmt_tiers).scalars().all()
        #         results_normal = list(filter(lambda tier: tier.isAddon==False, results))
        #         results_addon = list(filter(lambda tier: tier.isAddon==True, results))
        #         ## 找訂閱裡有匹配方案的對象
        #         ### >=價格的標準方案
        #         if len(results_normal) > 0:
        #             stmt_tier_normal = select(UserData).join(
        #                     UserSubscription, UserData.userID == UserSubscription.userID
        #                 ).where(
        #                 UserSubscription.creatorID == creator_id,
        #                 UserSubscription.subscription_Year == tw_datetime.strftime('%Y'),
        #                 UserSubscription.subscription_Month == tw_datetime.strftime('%m'),
        #                 UserSubscription.IsPay == True,
        #                 UserSubscription.cancelUser.is_(None),
        #                 UserSubscription.isAddon == False,
        #                 UserSubscription.price >= results_normal[0].price #only one
        #             ).order_by(UserSubscription.userID.asc())
        #             results_tier_normal = db.execute(stmt_tier_normal).scalars().all()
        #             results_tier_normal = list(map(lambda x: {'user_email': x.email, 'user_name': x.displayName}, results_tier_normal))
        #         else:
        #             results_tier_normal = []
        #         ### 等價的進階方案
        #         addon_list = list(map(lambda x:x.tierID, results_addon))
        #         if len(results_addon) > 0:
        #             stmt_tier_addon = select(UserData).join(
        #                     UserSubscription, UserData.userID == UserSubscription.userID
        #                 ).where(
        #                 UserSubscription.creatorID == creator_id,
        #                 UserSubscription.subscription_Year == tw_datetime.strftime('%Y'),
        #                 UserSubscription.subscription_Month == tw_datetime.strftime('%m'),
        #                 UserSubscription.IsPay == True,
        #                 UserSubscription.cancelUser.is_(None),
        #                 UserSubscription.isAddon == True,
        #                 UserSubscription.tierID.in_(addon_list)
        #             ).order_by(UserSubscription.userID.asc())
        #             results_tier_addon = db.execute(stmt_tier_addon).scalars().all()
        #             results_tier_addon = list(map(lambda x: {'user_email': x.email, 'user_name': x.displayName}, results_tier_addon))
        #         else:
        #             results_tier_addon = []
        #         results = [dict(t) for t in set([tuple(d.items()) for d in (results_tier_normal+results_tier_addon)])]
        #         ## 寄出email
        #         for tar in results:
        #             format_dict = mail_info.copy()
        #             format_dict.update(tar)
        #             print('to', format_dict)
        #             background_tasks.add_task(send_format_mail_ses, format_dict['user_email'], '[Clusters - 可洛斯·創作者集群] {} 的新作品通知！'.format(format_dict['creator_name']), format_dict)
        #         return {
        #             'detail': {'mailStatus': 'sending'}
        #         }

    else:
        return {
            'detail': {'mailStatus': 'no need'}
        }