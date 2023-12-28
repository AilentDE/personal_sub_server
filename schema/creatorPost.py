from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreatorPostSchema(BaseModel):
    id: str
    title: str|None = '新作品'
    layout: str
    thumbnailAssetId: str|None = ''
    thumbnailDisplayMode: str
    excerpt: str|None = ''
    bodyHtml: str|None = ''
    visibility: str
    visibleTierIds: List[str]|None = []
    creatorField: str
    albumAssetIds: List[str]|None = []
    attachmentAssetsIds: List[str]|None = ''
    externalMediaUrl: str|None = ''
    projectId: str|None = ''
    isNsfw: bool
    isPinned: bool
    tags: List[str]|None = []
    publishedAt: datetime
    projectTitle: str|None = ''
    creatorId: str|None = None
    isRecommend: bool = False
    viewsCount: int = 0