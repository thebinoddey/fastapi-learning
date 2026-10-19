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
    linkedin_profile: Annotated[Optional[AnyUrl], Field( description="LinkedIn profile URL")] = None
    salary: Annotated[float, Field(..., gt=0, strict=True, description="Salary in INR")]
    married: Annotated[bool, Field(..., description="Marital status of the employee")]
    skills: Annotated[List[str], Field(..., description="List of skills")] = []
    
    @computed_field
    @property
    def annualBonus(self) -> float:
        return self.salary * 0.2
    
#Update_Employee class is created

class Update_Employee(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['Male', 'Female', 'Other']], Field(default=None)]
    email: Annotated[Optional[EmailStr], Field(default=None)]
    contact_no: Annotated[Optional[str], Field(default=None)]
    address: Annotated[Optional[Address], Field(default=None)]
    linkedin_profile: Annotated[Optional[AnyUrl], Field(default=None)]
    salary: Annotated[Optional[float], Field(default=None, gt=0, strict=True)]
    married: Annotated[Optional[bool], Field(default=None)]
    skills: Optional[List[str]] = None
        
def load_data():
    with open("employee.json", "r") as f:
        data = json.load(f)
    return data

#Endpoint - Update (PUT) - Update employee details based on employee ID 
@app.put("/update/{eid}")
def update_employee(eid: int, employee_update: Update_Employee):
    data = load_data()
    
    #Check if employee exists
    if str(eid) not in data:
        raise HTTPException(status_code=404, detail=f"Employee with ID {eid} not found.")
    
    # Copy existing data so it isn't modified prematurely
    existing_employee_data = data[str(eid)]
    existing_employee_data['eid'] = eid 
    
    # Get only fields explicitly supplied by the client
    updated_info = employee_update.model_dump(exclude_unset=True, mode="python")
    
    #Merge the changes into copied record
    for key, value in updated_info.items():
        existing_employee_data[key] = value 
    
    
    ## Tricky part - model validators. annualBonus is a computed field, so we need to create an Employee object to recalculate it.
    
    
    emp_pydantic_object = Employee(**existing_employee_data)  
    # Recalculate computed fields
    emp_dict = emp_pydantic_object.model_dump(mode="json", exclude={"eid"})  # Convert back to dict for storage
    
    #add this dict to data
    data[str(eid)] = emp_dict
    
    # Save updated data
    with open("employee.json", "w") as f:
        json.dump(data, f)
    
    return JSONResponse(status_code=200, content={"message": f"Employee with ID {eid} updated successfully."})


@app.delete("/delete/{eid}")
def delete_employee(eid: int):
    data = load_data()
    
    #Check if employee exists
    if str(eid) not in data:
        raise HTTPException(status_code=404, detail=f"Employee with ID {eid} not found.")
    
    # Remove employee from data
    del data[str(eid)]
    
    # Save updated data
    with open("employee.json", "w") as f:
        json.dump(data, f)
    
    return JSONResponse(status_code=200, content={"message": f"Employee with ID {eid} deleted successfully."})
