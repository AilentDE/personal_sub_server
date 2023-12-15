from sqlalchemy import Column, String, NVARCHAR, Boolean, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class WorkData(Base):
    __tablename__ = 'Work'

    workID = Column(String(225), primary_key=True)
    title = Column(NVARCHAR)
    depiction = Column(NVARCHAR)
    userID = Column(String(225))
    workType = Column(String(225))
    bannerID = Column(String)
    bannerModel = Column(String(20))
    externalMediaURL = Column(String)
    publicSetting = Column(String(20))
    IsPublish = Column(Boolean)
    activityID = Column(String(225))
    browseCount = Column(Integer)
    publishTime = Column(DateTime)
    bodyHtml = Column(NVARCHAR)
    typeID = Column(String(225))
    isNSFW = Column(Boolean)
    isPinned = Column(Boolean)
    createTime = Column(DateTime)
    updateTime = Column(DateTime)
    isDelete = Column(Boolean, default=False)
    deleteTime = Column(DateTime)
    isRecommended = Column(Boolean)
