from sqlalchemy.orm import Session
from datetime import date
from . import models, schemas


def get_employee_time_sheet(db: Session, employee_time_sheet_id: int):
    return db.query(models.EmployeeTimeSheet).filter(models.EmployeeTimeSheet.id == employee_time_sheet_id).first()



def get_employee_time_sheet_logs(db: Session, employee_id:int, log_date:date, offset: int = 0, limit: int = 100):
    return db.query(models.EmployeeTimeSheet).filter(models.EmployeeTimeSheet.employee_id==employee_id).\
        filter(models.EmployeeTimeSheet.log_date==log_date).\
        offset(offset).limit(limit).all()


def create_employee_time_sheet_log(db: Session, employee_time_sheet_details: schemas.EmployeeTimeSheetCreateSchema):
    db_employee = models.EmployeeTimeSheet(employee_id=employee_time_sheet_details.employee_id,
                                           log_date=employee_time_sheet_details.log_date,
                                           hrs=employee_time_sheet_details.hrs)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee