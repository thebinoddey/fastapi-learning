
from fastapi import FastAPI, HTTPException
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
