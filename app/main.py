""" This is entry point for the app. It consist of CRUD api endpoints for employee table"""

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import Employee

app = FastAPI()

@app.on_event("startup")
def create_table():
    """This function creates table
    """
    Base.metadata.create_all(bind=engine)

@app.post("/employees/")
def create_employees(name: str, department: str, _db: Session = Depends(get_db)):
    """This function takes name, department and create employees

    Args:
        name (str): Name of the employee
        department (str): Name of the department
        db (Session, optional): Defaults to Depends(get_db).

    Raises:
        HTTPException: raises exception in case of bad request

    Returns:
        _type_: json format with {"Employee added": name}
    """
    try:
        employee = Employee(name= name, department= department)
        _db.add(employee)
        _db.commit()
        return {"Employees added": employee.name}
    except HTTPException as exce:
        raise exce(status_code = status.HTTP_400_BAD_REQUEST)


@app.get("/employees/")
def get_employees(_db: Session = Depends(get_db)):
    """This function returns employee

    Args:
        db (Session, optional): Defaults to Depends(get_db).

    Raises:
        HTTPException: raises exception in case of bad request

    Returns:
       _type_: json format with {"status": status_code, "employees": employees}
    """
    employees = _db.query(Employee).all()
    if not employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Employee not found")
    return {"status": status.HTTP_200_OK, "employees": employees}


@app.get("/employees/")
@app.get("/employees/{employee_id}")
def get_employee(employee_id: str = None, _db: Session = Depends(get_db)):
    """Get employees either by ID or all employees.

    Args:
        employee_id (str, optional): ID of the employee. Defaults to None.
        db (Session, optional): Database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: Raises 404 if employee(s) not found.

    Returns:
        dict: JSON response with status and employee data.
    """
    if employee_id:
        employee = _db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Employee with ID {employee_id} not found")
        return {"status": status.HTTP_200_OK, "employee": employee}
    employees = _db.query(Employee).all()
    if not employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Employees not found")
    return {"status": status.HTTP_200_OK, "employees": employees}


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str, _db: Session = Depends(get_db)):
    """This function takes employee_id and delete the record of that
    employee

    Args:
        employee_id (str): id of the employee
        db (Session, optional): Defaults to Depends(get_db).

    Raises:
        HTTPException: raises exception in case there are no employees

    Returns:
        _type_: json format with {"status": status_code}
    """
    employee_query = _db.query(Employee).filter(Employee.id == employee_id)
    employee = employee_query.first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with {employee_id} not found")
    employee_query.delete(synchronize_session=False)
    _db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)


@app.put("/employees/{employee_id}/{column}/{new_value}")
def update_employee(employee_id: str, column: str, new_value: str, _db: Session = Depends(get_db)):
    """This function takes in the employee id , column name and corresponding value
    and updates the record of the employee

    Args:
        employee_id (str): id of the employee
        column (str): column name 
        new_value (str): new value
        _db (Session, optional): Defaults to Depends(get_db).

    Raises:
        HTTPException: raises exception in case there are no employees

    Returns:
        _type_: json format with {"status": status_code, "employee": employee}
    """
    employee_query = _db.query(Employee).filter(Employee.id == employee_id)
    db_employee = employee_query.first()

    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Employee with id {employee_id} not found")

    setattr(db_employee, column, new_value)
    _db.add(db_employee)
    _db.commit()
    _db.refresh(db_employee)
    return {"status": "success", "employee": db_employee}
