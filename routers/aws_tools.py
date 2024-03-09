from fastapi import APIRouter, Body, Path
from fastapi.responses import RedirectResponse
from typing import Annotated
from utils.aws_tool import create_presigned_url

router = APIRouter(
    prefix='/aws',
    tags=['aws']
)

@router.post('/presignedUrl')
async def test_mail(bucketName:Annotated[str, Body()], objectName:Annotated[str, Body()], expiration:Annotated[int, Body()] = 3600):
    presigned_url = create_presigned_url(bucketName, objectName, expiration)
    return {
        'detail': {'presignedUrl': presigned_url}
    }

@router.get('/presignedUrl/file/{userId}/{objectName}')
async def get_presigned_url_for_avatar(userId:Annotated[str, Path()], objectName:Annotated[str, Path()]):
    bucketName = 'clusters-assets-bucket'
    objectName = userId + '/' + objectName + '/blob'
    presigned_url = create_presigned_url(bucketName, objectName)
    return RedirectResponse(presigned_url)