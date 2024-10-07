import os
import time
from groq import Groq

class GroqChat:
    def __init__(self):
        self.groq_api_key = "" #Enter the Groq API Key
        self.client = Groq(api_key=self.groq_api_key)
        self.chat_history = [] # to keep track of the history
    
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
        
        return
    


if __name__ == "__main__":
    groq_obj = GroqChat()
    print("Staring chat session...")
    groq_obj.ChatSession()
