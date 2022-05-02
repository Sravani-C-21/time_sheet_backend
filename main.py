from typing import List
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from db import crud, models, schemas
from db.database import SessionLocal, engine
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import requests
from config import employee_service_host, get_employee_url
from datetime import date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/employee_time_sheet/", response_model=schemas.EmployeeTimeSheetResponseSchema)
def create_employee_time_sheet(employee_time_sheet: schemas.EmployeeTimeSheetCreateSchema, db: Session = Depends(get_db)):
    try:
        url = employee_service_host + get_employee_url + str(employee_time_sheet.employee_id)
        response = requests.get(url)
        _json = response.json()
        print("response==", response.json())
        if _json and _json.get('id')!=employee_time_sheet.employee_id:
            return JSONResponse(status_code=400, content={"error":"Employee id does not exists."})
        db_employee = crud.create_employee_time_sheet_log(db=db, employee_time_sheet_details=employee_time_sheet)
        json_compatible_item_data = jsonable_encoder(db_employee)
        return JSONResponse(content=json_compatible_item_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e.orig))

@app.get("/employee_time_sheet/{employee_time_sheet_id}", response_model=schemas.EmployeeTimeSheetResponseSchema)
def get_employee_time_sheet(employee_time_sheet_id: int, db: Session = Depends(get_db)):
    db_employee_time_sheet = crud.get_employee_time_sheet(db, employee_time_sheet_id=employee_time_sheet_id)
    if not db_employee_time_sheet:
        raise HTTPException(status_code=400, detail="Employee time sheet does not exist with given id")
    json_compatible_item_data = jsonable_encoder(db_employee_time_sheet)
    return JSONResponse(content=json_compatible_item_data)


@app.get("/employee_time_sheet/", response_model=schemas.EmployeeTimeSheetResponseSchema)
def list_employees(employee_id:int, log_date: date, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employee_time_sheet_logs = crud.get_employee_time_sheet_logs(db, employee_id=employee_id,
                                                                 log_date = log_date,
                                                                 offset=offset, limit=limit)
    json_compatible_item_data = jsonable_encoder(employee_time_sheet_logs)
    return JSONResponse(content=json_compatible_item_data)


if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)