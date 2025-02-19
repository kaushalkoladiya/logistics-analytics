from pydantic import BaseModel, field_validator
from datetime import datetime


class DateRangeBase(BaseModel):
    start: str
    end: str

    @field_validator("start", "end")
    @classmethod
    def validate_date(cls, v: str) -> datetime:
        try:
            return datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

    @field_validator("end")
    @classmethod
    def validate_date_range(cls, end_date: datetime, info) -> datetime:
        if "start" in info.data and end_date < info.data["start"]:
            raise ValueError("End date must be after start date")
        return end_date
