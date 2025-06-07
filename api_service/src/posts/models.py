from sqlalchemy import String, Text, DateTime
from src.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Post(Base):
    title: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
