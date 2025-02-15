from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.db.session import Base


class SystemStatus(Base):
    __tablename__ = "system_status"

    id = Column(Integer, primary_key=True, index=True)
    is_calculating = Column(Boolean, default=False)
    started_calculating_at = Column(DateTime(timezone=True), nullable=True)
    last_calculated_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(String, nullable=True)
