#Knows how to draw the terminal.
from backend import chat_stream

history = [] 

while True:
    user_input = input("Calvin: ")
    history.append({"role": "user", "content": user_input})

    print("AI: ", end="", flush=True) 
    #without flush=True, it might wait until the whole response is done before printing anything, which would defeat the purpose of streaming.
    
    full_reply = ""

    for chunk in chat_stream(history):
        print(chunk, end="", flush=True) 
        full_reply += chunk

    print() #after the stream is done, move to the next line for the user input.

    history.append({"role": "assistant", "content": full_reply})