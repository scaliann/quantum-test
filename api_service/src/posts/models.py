from sqlalchemy import String, Text, DateTime
from src.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timedelta, timezone


def utc_plus_3() -> datetime:
    """Возвращает текущее время + 3 ч, привязанное к UTC+3."""
    return datetime.now(timezone.utc) + timedelta(hours=3)


class Post(Base):
    title: Mapped[str] = mapped_column(String(255))
    text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_plus_3)
