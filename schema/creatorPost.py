from pydantic import BaseModel
from typing import List
from datetime import datetime

class CreatorPostSchema(BaseModel):
    title: str
    layout: str
    thumbnailAssetId: str
    thumbnailDisplayMode: str
    excerpt: str
    bodyHtml: str
    visibility: str
    visibleTierIds: List[str]
    creatorField: str
    albumAssetIds: List[str]
    attachmentAssetsIds: List[str]
    externalMediaUrl: str
    projectId: str
    isNsfw: bool
    isPinned: bool
    tags: List[str]
    publishedAt: datetime