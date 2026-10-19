
from fastapi import FastAPI, HTTPException, Query
import json

app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Welcome"}


@app.get("/about")
def about():
    return {"message": "This is an employee database!"}


def load_data():
    with open("employee.json", "r") as f:
        data = json.load(f)
    return data


@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    data = load_data()

    employee = next(
        (emp for emp in data if emp["eid"] == employee_id),
        None
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@app.get("/sort")
def sort_employees(sort_by: str = Query(..., description="Field to sort by (eid, ename, dept, join_date)"), order: str = Query("asc", description="Sort order (asc or desc)")):
    
    valid_fields = ["eid", "ename", "dept", "join_date"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort order. Select between ascending (asc) or descending (desc)"
        )
        
    data = load_data()
        
    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=(order == "desc"))
    return sorted_data
