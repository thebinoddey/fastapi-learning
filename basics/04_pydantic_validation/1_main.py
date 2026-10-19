from pydantic import BaseModel, Field

class Employee(BaseModel):
    eid: int
    ename: str
    dept: str
    join_date: str
    
def insert_employee(employee: Employee):
    print(f"Employee ID: {employee.eid}")
    return {"message": "Employee inserted successfully", "employee": employee.model_dump()}

employee_info = {'eid': 101, 'ename': 'John Doe', 'dept': 'IT', 'join_date': '2023-01-15'}
e1 = Employee(**employee_info)

insert_employee(e1)