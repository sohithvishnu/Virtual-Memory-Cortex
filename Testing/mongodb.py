from pymongo import MongoClient
from pydantic import BaseModel, Field
from datetime import date
import uuid
from typing import List

# 1. Define the Models 
class Message(BaseModel):
    role: str
    content: str

class Thread(BaseModel):
    # Use default_factory so these auto-generate every time a new Thread is created
    session_ID: str = Field(default_factory=lambda: str(uuid.uuid4()))
    intialized_date: date = Field(default_factory=date.today)
    # We nest the messages inside the thread
    messages: List[Message] = []

def run_database_test():
    print("Connecting to local MongoDB...")
    
    # 2. Connect to local MongoDB 
    # (Ensure your local MongoDB service is running via Windows Services or mongod)
    client = MongoClient("mongodb://localhost:27017/")
    
    # Create/Access the 'cortex_test' database and 'threads' collection
    db = client.cortex_test
    threads_collection = db.threads

    # 3. Create our Python Objects
    print("Creating Thread and Messages in Python...")
    msg1 = Message(role="user", content="Good morning, Cortex. What's on the agenda?")
    msg2 = Message(role="assistant", content="Good morning! Your daily thread is initialized.")
    
    # Initialize the thread with our messages
    daily_thread = Thread(messages=[msg1, msg2])
    
    # 4. Insert into MongoDB
    # Pydantic v2 uses .model_dump() to convert the object into a Python dictionary that Mongo accepts
    document_to_insert = daily_thread.model_dump()
    
    # Convert the date object to a string so Mongo plays nicely with it
    document_to_insert['intialized_date'] = document_to_insert['intialized_date'].isoformat()
    
    result = threads_collection.insert_one(document_to_insert)
    print(f"✅ Success! Inserted Thread Document ID: {result.inserted_id}")

    # 5. Retrieve from MongoDB to prove it worked
    print("\n🔍 Retrieving the exact document back from MongoDB:")
    retrieved_doc = threads_collection.find_one({"session_ID": daily_thread.session_ID})
    
    import pprint
    pprint.pprint(retrieved_doc)

    # Optional: Clean up after test
    # threads_collection.delete_one({"session_ID": daily_thread.session_ID})

if __name__ == "__main__":
    run_database_test()