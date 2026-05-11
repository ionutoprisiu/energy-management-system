from sqlalchemy import Column, Float, Integer, String

from app.db.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    max_consumption = Column(Float, nullable=False)
    user_id = Column(Integer, index=True, nullable=True)
