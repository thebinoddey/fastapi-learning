from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated

class Employee(BaseModel): 
    name: str
    age: int = Field(gt=0)
    email: EmailStr
    linkedin_profile: Optional[AnyUrl] = None
    salary: float = Field(gt=0)
    married: bool
    skills: List[str]
    
    @computed_field
    @property
    def annualBonus(self) -> float:
        return self.salary * 0.2
    
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
print(employee1.name)
print(employee1.annualBonus)

