from fastapi import FastAPI
from typing import Optional, List
from pydantic import BaseModel;
import requests
app=FastAPI()

class bloodapi_readings(BaseModel):
   result_type: str
   name: str
   time_collected:Optional[str] = None
   result:  float
   unit_of_measure: str
   range_minimum: Optional[float] = None
   range_maximum: Optional[float] = None
   comments: Optional[str] = None
   rejection_reason: Optional[str] = None    

class bloodapi(BaseModel):
   results:List[bloodapi_readings]

@app.post("/")
def get_result(payload:bloodapi):      
    return "data send successfully"
 
