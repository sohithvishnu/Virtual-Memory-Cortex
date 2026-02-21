from ollama import chat, Client
from ollama import ChatResponse
from utils import Message
from config import system_prompt

class llmInferenceEngine():
    def __init__(self, model_name):
        # Intialize the model
        self.client = Client(host='http://localhost:11434', headers={'x-some-header': 'some-value'})
        self.model = model_name

    def response(self,input_msg):
        response_assistant =  self.client.chat(model = self.model, messages=input_msg)
        return Message(role=response_assistant.message.role, content=response_assistant.message.content)
    


if __name__ == "__main__":
    print("Creating Thread and Messages in Python...")
    msg1 = Message(role="user", content="Good morning, Cortex. What's on the agenda?")
    msg0 = Message(role="system", content=system_prompt)
    final_msg = [msg0,msg1]
    print(final_msg)
    llm = llmInferenceEngine("llama3.1")
    print(llm.response(final_msg))


