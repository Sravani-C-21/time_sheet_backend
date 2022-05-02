from typing import List, Optional
from datetime import date

from pydantic import BaseModel


class EmployeeTimeSheetCreateSchema(BaseModel):
    employee_id: int
    log_date: date
    hrs: Optional[float] = None


class EmployeeTimeSheetResponseSchema(BaseModel):
    id: int
    employee_id: str
    log_date: date
    hrs: Optional[float] = None