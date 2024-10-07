import os
import time
from groq import Groq

class GroqChat:
    def __init__(self,window_size=5):
        self.groq_api_key = ""
        self.client = Groq(api_key=self.groq_api_key)
        self.chat_history = [] # to keep track of the history
        self.window_size = window_size * 2
    
    def ChatSession(self):
        
        while True: # chat session to keep going on till the user dont exit the application
            self.user_input = input("Enter query: ")
            
            #condition to stop the chat session
            if self.user_input.lower()=="exit":
                print("chat session ended")
                break

            #Maintain user prompt history
            self.chat_history.append({"role":"user","content":self.user_input})

            #Call Groq API to get response
            self.chat_completion = self.client.chat.completions.create(messages=self.chat_history,model="llama3-8b-8192")

            #Get the actual response message
            self.response_message = self.chat_completion.choices[0].message.content

            #Maintain the response history
            self.chat_history.append({"role":"user","content":self.response_message})

            print(self.response_message)
            print("\n")

            #keep checking for the window buffer size
            self.SlidingWindowMemmory()

            print("length of the chat history is: "+str(len(self.chat_history)))
        
        return
    
    #Keep track of the window for the memory
    def SlidingWindowMemmory(self):
        if(len(self.chat_history)>=self.window_size):
            self.chat_history = self.chat_history[-self.window_size:] #forget the conversations beyong the memory size
            return self.chat_history

if __name__ == "__main__":
    groq_obj = GroqChat(3) #pass in the window size
    print("Staring chat session...")
    groq_obj.ChatSession()
