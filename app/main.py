from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Employee

app = FastAPI()

@app.on_event("startup")
def create_table():
    # Create all tables defined in Base's metadata
    Base.metadata.create_all(bind=engine)

@app.post("/employees/")
def create_employees(name: str, department: str, db: Session = Depends(get_db)):
    employee = Employee(name= name, department= department)
    db.add(employee)
    db.commit()
    return {"Employees added": employee.name}

@app.get("/employees/")
def get_employees(db: Session = Depends(get_db)):
    employees = db.query(Employee).all()
    return {"status": "success", "employees": employees}

@app.get("/employees/{employee_id}")
def get_employees(employee_id: str, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with {employee_id} not found")
    
    return {"status_code": status.HTTP_200_OK, "employee": employee}

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    employee_query = db.query(Employee).filter(Employee.id == employee_id)
    employee = employee_query.first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with {employee_id} not found")
    
    employee_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@app.put("/employees/{employee_id}/{column}/{new_value}")
def update_employee(employee_id: str, column: str, new_value: str, db: Session = Depends(get_db)):
    employee_query = db.query(Employee).filter(Employee.id == employee_id)
    db_employee = employee_query.first()

    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with id {employee_id} not found")

    setattr(db_employee, column, new_value) # Set the new value for the specified column
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    
    return {"status": "success", "employee": db_employee}

    






    