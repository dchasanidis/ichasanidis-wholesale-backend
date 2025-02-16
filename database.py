import os
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import declarative_base, sessionmaker

# Get database credentials from environment variables or use default values
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mysecretpassword")
DB_NAME = os.getenv("DB_NAME", "ichasanidis_images")
DB_PORT = os.getenv("DB_PORT", "5432")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Image(Base):
    __tablename__ = "images"
    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    location = Column(String)
    origin_filename = Column(String)

    business_id = Column(String, index=True)
    title = Column(String)
    description = Column(String)

    def to_dict(self):
        return {
            "id": self.id,
            "origin_filename": self.origin_filename,
            "business_id": self.business_id,
            "title": self.title,
            "description": self.description
        }

class ImageMetadata(BaseModel):
    business_code: str
    title: str
    description: str

Base.metadata.create_all(bind=engine)
