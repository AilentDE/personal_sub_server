from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreatorPostSchema(BaseModel):
    id: str
    title: str|None = None
    layout: str
    thumbnailAssetId: str|None = None
    thumbnailDisplayMode: str
    excerpt: str = ''
    bodyHtml: str = ''
    visibility: str
    visibleTierIds: List[str] = []
    creatorField: str
    albumAssetIds: List[str] = []
    attachmentAssetsIds: List[str] = ''
    externalMediaUrl: str|None = ''
    projectId: str|None = ''
    isNsfw: bool
    isPinned: bool
    tags: List[str] = []
    publishedAt: datetime
    projectTitle: str|None = ''
    creatorId: str|None = None
    isRecommend: bool = False
    viewsCount: int = 0