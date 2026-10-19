from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class Employee(BaseModel): 
    name: str
    age: int = Field(gt=0)
    email: EmailStr
    linkedin_profile: Optional[AnyUrl] = None
    salary: float = Field(gt=0)
    married: bool
    skills: List[str]
    
    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        
        valid_domains = ["amazon.com","google.com", "microsoft.com"]
        domain_name = value.split("@")[-1]
        
        if domain_name not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
    
    @field_validator("name")   
    @classmethod
    def transform_name(cls, value):
        return value.title ()


def insert_employee(employee: Employee):
    return {"message": "Employee inserted successfully", "employee": employee.model_dump()}   
    
employee_info = { 
    'name': 'John Doe',
    'age': 54,
    'email': 'john.doe@microsoft.com',
    'linkedin_profile': 'https://www.linkedin.com/in/johndoe',
    'salary': 75000.0,
    'married': True,
    'skills': ['Python', 'FastAPI']
}       
    
employee1 = Employee(**employee_info)
insert_employee(employee1)
print(employee1.model_dump())

