from sqlalchemy import Column, String, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserSubscriptionPurview(Base):
    __tablename__ = "UserSubscriptionPurview"

    userID = Column(String(255), primary_key=True, nullable=False)
    creatorID = Column(String(255), primary_key=True, nullable=False)
    tierID = Column(String(255), primary_key=True, nullable=False)
    subscription_Year = Column(String(4), primary_key=True, nullable=False)
    subscription_Month = Column(String(2), primary_key=True, nullable=False)
    createTime = Column(DateTime)
    price = Column(Integer)
    isAddon = Column(Boolean)