from sqlalchemy.orm import Session
from datetime import datetime

from app.db.session import SessionLocal
from app.models.system_status import SystemStatus


class CalculationStatusService:
    def __init__(self):
        self.db: Session = SessionLocal()
        self.create_table()

    def create_table(self):
        SystemStatus.__table__.create(bind=self.db.bind, checkfirst=True)

    def get_system_status(self):
        status = self.db.query(SystemStatus).first()
        if not status:
            return {
                "is_calculating": False,
                "last_calculated_at": None,
                "error_message": None,
            }
        return {
            "is_calculating": status.is_calculating,
            "last_calculated_at": status.last_calculated_at,
            "error_message": status.error_message,
        }

    def mark_calculation_start(self):
        status = self.db.query(SystemStatus).first()
        if not status:
            status = SystemStatus()
            self.db.add(status)

        status.is_calculating = True
        status.error_message = None
        status.started_calculating_at = datetime.utcnow()
        self.db.commit()

    def mark_calculation_end(self, success: bool = True, error: str = None):
        status = self.db.query(SystemStatus).first()
        if status:
            status.is_calculating = False
            status.last_calculated_at = datetime.utcnow()
            status.error_message = error if not success else None
            self.db.commit()
