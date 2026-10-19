from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Employee(BaseModel): 
    name: Annotated[str, Field(max_length=80, title="Full Name",description="Full name of the employee", example=["Jai", "Farhan"])]
    age: int = Field(gt=0, description="Age of the employee")
    email: EmailStr = Field(description="Email address of the employee")
    linkedin_profile: Optional[AnyUrl] = None
    salary: float = Field(gt=0, strict=True, description="Salary in INR")
    married: bool = Field(description="Marital status of the employee")
    skills: List[str] = Field(default_factory=list, description="List of skills")

def insert_employee(employee: Employee):
    return {"message": "Employee inserted successfully", "employee": employee.model_dump()}   
    
employee_info = { 
    'name': 'John Doe',
    'age': 54,
    'email': 'john.doe@example.com',
    'linkedin_profile': 'https://www.linkedin.com/in/johndoe',
    'salary': 75000.0,
    'married': True,
    'skills': ['Python', 'FastAPI']
}       
    
employee1 = Employee(**employee_info)
insert_employee(employee1)

