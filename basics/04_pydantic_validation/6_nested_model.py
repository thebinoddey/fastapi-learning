from pydantic import BaseModel

class Address(BaseModel):
    city: str
    state: str
    pin_code: str
    
class Employee(BaseModel):
    eid: int
    ename: str
    gender: str
    dept: str
    salary: float
    address: Address
    
address_dict = {'city': 'Jaipur', 'state': 'Rajasthan', 'pin_code': '302031'}
address1 = Address(**address_dict)

employee_info = {'eid': 101, 'ename': 'John Doe', 'gender': 'Male', 'dept': 'IT', 'salary': 75000.0, 'address': address1}
e1 = Employee(**employee_info)

print(e1.address.pin_code) #302031

