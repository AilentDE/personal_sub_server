from sqlalchemy import Column, String, Integer, DateTime, Boolean, Date, Float, NVARCHAR, SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserData(Base):
    __tablename__ = "UserData"

    userID = Column(String(255), primary_key=True, nullable=False)
    displayName = Column(NVARCHAR(255))
    tel = Column(String(20))
    email = Column(String(255))
    birthday = Column(Date)
    password = Column(String(255))
    externalUrl = Column(String)
    showNSFW = Column(Boolean)
    locale = Column(NVARCHAR)
    createdAt = Column(DateTime)
    lastSignedInAt = Column(DateTime)
    avatarAssetID = Column(String(225))
    creatorBannerAssetID = Column(String(225))
    isWork = Column(Boolean)
    isAdmin = Column(Boolean)
    UTC = Column(SmallInteger)
    isRecommended = Column(Boolean)
    platformFeePercent = Column(Float(53))
    creditToken = Column(String(255))
    balance = Column(Integer)
    isDisable = Column(Boolean)
    creditNo = Column(String(4))