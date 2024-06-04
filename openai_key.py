from openai import OpenAI
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

app=FastAPI()
client = OpenAI()
# client.api_key = os.getenv("OPENAI_API_KEY")    

class chat_prompt(BaseModel):
    user_prompt:str

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
   
   
chat_history = [
            # {"role": "system", "content": ""},          
        ]

@app.post("/chat")
async def chat_endpoint(payload:chat_prompt):
    chat_history.append({"role": "user", "content": payload.user_prompt})

    try:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )        
        response=completion.choices[0].message.content
        chat_history.append({"role":"assistant","content":response})
        print(chat_history) 
        return response
    
    except Exception as e:
            
       return "Something went wrong! :( "
        
            
@app.post("/create")     
async def prompt_template(payload:bloodapi): 
    chat_history.clear()
    prompt_template={"role":"system","content":f'You are a test report bot,you will be responding to provided data:{payload.results},only respond to queries based on data as per your role, else refuse'}  
    chat_history.append(prompt_template)  
    print(chat_history) 
    return "persona created"
          
    