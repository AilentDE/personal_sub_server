from sqlalchemy import Column, String, NVARCHAR, Boolean, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FileList(Base):
    __tablename__ = 'FileList'

    CreatorID = Column(String(225), primary_key=True, nullable=False)
    fileID = Column(String(225), primary_key=True, nullable=False)
    fileName = Column(NVARCHAR)
    filePath = Column(NVARCHAR)
    contentType = Column(NVARCHAR)
    label = Column(NVARCHAR(255))
    crop = Column(Boolean)
    updateTime = Column(DateTime)
    width = Column(Integer)
    height = Column(Integer)
    size = Column(Integer)
    isDelete = Column(Boolean)