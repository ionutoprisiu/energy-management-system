from app.db.database import Base
from sqlalchemy import Column, Integer, String

class Credential(Base):
    __tablename__ = "credentials"
    id = Column(Integer, primary_key=True, index=True)
    username= Column(String, unique=True, index=True, nullable=False)
    hashed_password= Column(String, nullable=False)
    role= Column(String, index=True, nullable=False)