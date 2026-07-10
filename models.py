import datetime
from sqlalchemy import Column, String, Boolean, Integer, Text, DateTime
from database import Base


class Listing(Base):
    __tablename__ = "listings"

    id = Column(String, primary_key=True, index=True)
    type = Column(String, nullable=False)          # 'App', 'Website', 'CRM'
    status = Column(String, nullable=False)        # 'Live', 'InDev', 'Concept'
    title = Column(String, nullable=False)
    tagline = Column(String, default="")
    desc = Column(Text, default="")
    stack = Column(String, default="")             # Stored as JSON-encoded list internally
    sku = Column(String, unique=True, index=True)
    previewType = Column(String, default="image")  # 'image' or 'video'
    link = Column(String, default="")
    previewUrl = Column(String, default="")
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, index=True)


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    interest = Column(String, default="Not sure yet")
    message = Column(Text, nullable=False)
    timestamp = Column(String, nullable=False)
    read = Column(Boolean, default=False)
