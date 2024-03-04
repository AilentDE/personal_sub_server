from pydantic import BaseModel, PlainSerializer
from typing import List, Dict
from typing_extensions import Annotated
from decimal import Decimal
# from datetime import datetime

class UserData(BaseModel):
    id: str
    displayName: str
    tel: str|None
    email: str
    showNsfw: bool
    locale: str|None
    avatarAssetId: str|None
    creatorBannerAssetId: str|None
    creatorFields: List[str]
    dateOfBirth: str|None
    createdAt: str # DynamoDB not support datetime type
    lastSignedInAt: str # DynamoDB not support datetime type
    socialMediaHandles: Dict[str, str]|None
    externalUrl: List[str]
    isGovIdVerified: str|None
    platformFeePercent: Annotated[
        Decimal,
        PlainSerializer(
            lambda x: float(x), return_type=float, when_used='json'
        ),
    ]
    isRecommended: bool
    isDisable: bool
    balance: int
    lastUpdatedAt: int # DynamoDB not support datetime type
