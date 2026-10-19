from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict, Optional, Annotated

class Employee(BaseModel): 
    name: str
    age: int = Field(gt=0)
    email: EmailStr
    linkedin_profile: Optional[AnyUrl] = None
    salary: float = Field(gt=0)
    married: bool
    skills: List[str]
    
    @model_validator(mode="after")
    def validate_email_domain(cls, values):
        email = values.get("email")
        valid_domains = ["amazon.com","google.com", "microsoft.com"]
        domain_name = email.split("@")[-1]
        
        if domain_name not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        
        return values
    
    
    
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

