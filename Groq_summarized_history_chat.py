import os
import time
from groq import Groq

class GroqChat:
    def __init__(self,window_size=5):
        self.groq_api_key = ""
        self.client = Groq(api_key=self.groq_api_key)
        self.chat_history = [] # to keep track of the history
        self.window_size = window_size * 2
        self.append_status = True #as long as this is true then keep appending the memory
        self.response_message = "" #this will hold the model response
        self.summarized_conversation = "" #at the first iteration, there is no summary
    
    def ChatSession(self):
        
        while True: # chat session to keep going on till the user dont exit the application

            self.user_input = input("\nEnter query: ")
            
            #condition to stop the chat session
            if self.user_input.lower()=="exit":
                print("chat session ended")
                break

            if(self.append_status==True):
                #Maintain user prompt history
                self.chat_history.append({"role":"user","content":self.user_input})

                #Call Groq API to get response
                self.chat_completion = self.client.chat.completions.create(messages=self.chat_history,model="llama3-8b-8192")

                #Get the actual response message
                self.response_message = self.chat_completion.choices[0].message.content

                #Maintain the response history
                self.chat_history.append({"role":"assistant","content":self.response_message})

                print(self.response_message)
                print("\n")

                print("length of the chat history is: "+str(len(self.chat_history)))

                if(len(self.chat_history)==self.window_size):
                    self.append_status = False
                    self.SummarizeHistory("","")

            else: #enter into summarization mode
                
                #self.SummarizeHistory(self.user_input,self.response_message)
                subsequent_summarization_prompt = f"{self.summarized_conversation}\n -----------------------------\nThe above is sumamrized conversation so far between the user and the assitant. Using this information, help answer the following following up query by the user: {self.user_input}"
                self.summarized_chat_completion = self.client.chat.completions.create(messages=[{"role": "user", "content": subsequent_summarization_prompt}],model="llama3-8b-8192")
                self.response_message = self.summarized_chat_completion.choices[0].message.content

                print("subsequent_summarization_prompt: "+str(subsequent_summarization_prompt)+"\n")
                print("In sumamrized mode, model response is below: ")
                print(self.response_message)
                print("\n")

                self.SummarizeHistory(self.user_input,self.response_message)#with the new prompt and response, update the summary once again

        return
            

    def SummarizeHistory(self,user_input,response_message):
        if(len(self.chat_history)>0): #window is full hence sumamrize that first and delete the window
            
            conversation_message = self._construct_conversation_message() #create a string for the conversation
            self.chat_history = [] # clear off the buffer
            summarization_prompt = f"Summarize the following conversation between the user and the assistant:\n\n{conversation_message}"
            self.summarized_conversation_call = self.client.chat.completions.create(messages=[{"role": "system", "content": summarization_prompt}],model="llama3-8b-8192")
            self.summarized_conversation = self.summarized_conversation_call.choices[0].message.content
            print("summarized conversation 1 is as follows: "+str(self.summarized_conversation))
            
        else:
            subsequent_summarization_prompt = f"{self.summarized_conversation}\n The above is sumamrized conversation so far between the user and the assitant. Using this and the latest user input and model response below, create a new consice summary\n User:{user_input},Assistant:{response_message}\n"
            self.summarized_conversation_call = self.client.chat.completions.create(messages=[{"role": "system", "content": subsequent_summarization_prompt}],model="llama3-8b-8192")
            self.summarized_conversation = self.summarized_conversation_call.choices[0].message.content
            print("summarized conversation is as follows: "+str(self.summarized_conversation))

    #Function to create the intitial conversation message
    def _construct_conversation_message(self):

        #Create the conversation message first
        conversation_message = ""
        for role_and_message in self.chat_history:
            role, message = role_and_message["role"], role_and_message["content"]
            conversation_message += f"{role}: {message}\n"
        return conversation_message

if __name__ == "__main__":
    groq_obj = GroqChat(2) #pass in the window size
    print("Staring chat session...")
    groq_obj.ChatSession()
