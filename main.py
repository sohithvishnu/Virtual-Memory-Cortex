import llm 
from utils import Message
from pymongo import MongoClient
from config import system_prompt
from pydantic import BaseModel, Field
from datetime import date
from typing import List
import uuid


client = MongoClient("mongodb://localhost:27017/")
db = client.cortex_test
threads_collection = db.threads
last_ten_conv = []
class Thread(BaseModel):
    # Use default_factory so these auto-generate every time a new Thread is created
    session_ID: str = Field(default_factory=lambda: str(uuid.uuid4()))
    intialized_date: date = Field(default_factory=date.today)
    system_prompt: str
    # We nest the messages inside the thread
    messages: List[Message] = []

class Memory_Manager():
    def __init__(self, memory_buffer_window):
        self.memory = []
        self.memory_buffer_window = memory_buffer_window
    
    def add_to_memory(self, mem_fragment):
        self.memory.append(mem_fragment)

    def rem_from_memory(self):
        if len(self.memory) > self.memory_buffer_window:
            self.memory.pop(0)

    def read_memory(self):
        return self.memory

memory = Memory_Manager(10)
llm_engine = llm.llmInferenceEngine("llama3.1")
while True:
    
    print("Creating Thread and Messages in Python...")
    input_msg = input(">")
    past_context = memory.read_memory()
    msg_user = Message(role="user", content=input_msg)
    msg0 = Message(role="system", content=system_prompt)
    final_msg = [msg0] + past_context + [msg_user]
    print(final_msg)

    response_msg = llm_engine.response(final_msg)
    daily_thread = Thread(system_prompt=msg0.content, messages=[msg_user,response_msg])
    for msg in daily_thread.messages:
        memory.add_to_memory(msg)
        memory.rem_from_memory()
    memory.rem_from_memory()
    document_to_insert = daily_thread.model_dump()
    document_to_insert['intialized_date'] = document_to_insert['intialized_date'].isoformat()
    result = threads_collection.insert_one(document_to_insert)
    print(f"✅ Success! Inserted Thread Document ID: {result.inserted_id}")




