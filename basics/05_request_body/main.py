from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated, Literal
import json

app = FastAPI()

class Address(BaseModel):
    city: str
    state: str
    pin_code: str
    
class Employee(BaseModel):
    eid: Annotated[int, Field(..., gt=0, description="Employee ID")]
    name: Annotated[str, Field(..., max_length=80, title="Full Name", description="Full name of the employee", example=["Jai", "Farhan"])]
    age: Annotated[int, Field(gt=0, description="Age of the employee")]
    gender: Annotated[Literal['Male', 'Female', 'Other'], Field(..., description="Gender of the employee")]
    email: Annotated[EmailStr, Field(..., description="Email address of the employee")]
    contact_no: Annotated[str, Field(..., description="Contact number of the employee")]
    address: Annotated[Address, Field(..., description="Address of the employee")]
    linkedin_profile: Annotated[Optional[AnyUrl], Field(None, description="LinkedIn profile URL")] = None
    salary: Annotated[float, Field(..., gt=0, strict=True, description="Salary in INR")]
    married: Annotated[bool, Field(..., description="Marital status of the employee")]
    skills: Annotated[List[str], Field(..., description="List of skills")] = []
    
    @computed_field
    @property
    def annualBonus(self) -> float:
        return self.salary * 0.2
    

@app.post("/create")
def create_employee(employee: Employee):
    
    def load_data():
        with open("employee.json", "r") as f:
            data = json.load(f)
        return data

    #load existing data
    data = load_data()
    
    #check if the record exists
    if str(employee.eid) in data:
        raise HTTPException(status_code=400, detail=f"Employee with ID {employee.eid} already exists.")
    
    #new employee added to db
    data[str(employee.eid)] = employee.model_dump(mode="json")
    
    #save updated data
    with open("employee.json", "w") as f:
        json.dump(data, f)
    
    return JSONResponse(status_code=201, content={"message": f"Employee with ID {employee.eid} created successfully."})
