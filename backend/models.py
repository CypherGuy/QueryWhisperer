from sqlalchemy import Column, Integer, String, Boolean
from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False,
                      index=True)  # Indexing helps with speed when searching
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False,
                       default=True)
    openai_api_key = Column(String, nullable=True)
