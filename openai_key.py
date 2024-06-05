from openai import OpenAI
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from dotenv import load_dotenv
load_dotenv()
os.getenv("OPENAI_API_KEY")   


app=FastAPI()
client = OpenAI()
origins = [
    "http://localhost:5500",
    "http://localhost:8080",
    "http://127.0.0.1:5500"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) 
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
   
chat_history =[]

async def chat_stream(chat_history):
    
        completion=client.chat.completions.create(
            model="gpt-4",
            messages=chat_history,
            stream=True
            )     
        for chunk in completion:       
            if chunk.choices[0].delta.content is not None:
                response=chunk.choices[0].delta.content
                chat_history.append({"role":"assistant","content":response})
                yield f"data: {chunk.choices[0].delta.content}\n\n"
                print(response) 
            

@app.post("/chat")
async def chat_endpoint(payload:chat_prompt):
    chat_history.append({"role": "user", "content": payload.user_prompt})
    return StreamingResponse(chat_stream(chat_history), media_type="text/event-stream")  
        
            
@app.post("/create")     
async def prompt_template(payload:bloodapi): 
    chat_history.clear()
    prompt_template={"role":"system","content":f'You are a test report bot,you will be responding to provided data:{payload.results},only respond to queries based on data as per your role, else refuse'}  
    chat_history.append(prompt_template)  
    print(chat_history) 
    return "persona created"
          
    