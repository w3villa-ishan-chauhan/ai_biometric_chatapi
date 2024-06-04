from fastapi import FastAPI
from typing import Optional ,List
from pydantic import BaseModel
app=FastAPI()
# class numberProvider:
#     number:[Optional]=0
#     @classmethod
#     def returnNumber(cls):
#         return cls.number
    
#     @classmethod
#     def setNumber(cls,new_number):
#         cls.number=new_number
class Employee(BaseModel):
    name:str
    age:int
class EmployeeList(BaseModel):
    department:List[Employee]
@app.post("/")
def post_number(payload:EmployeeList):   
   try:
        print(payload.department)
        return {"number set successfully"}
   except:
       print("Error occured")
# @app.get("/")
# def get_method():
#     number=numberProvider.returnNumber()
#     return {"number":number}



