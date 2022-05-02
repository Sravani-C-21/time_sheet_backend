from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DATE, FLOAT
from datetime import date
from .database import Base


class EmployeeTimeSheet(Base):
    __tablename__ = "employee_time_sheet"
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=True)
    log_date = Column(DATE, nullable=False, default=date.today())
    hrs = Column(FLOAT, nullable=True)