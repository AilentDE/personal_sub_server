from fastapi import APIRouter, Body
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