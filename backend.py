#Knows how to talk to the AI. backend.py is never run directly. It's a library. 
#You run streamlit run app.py or python cli.py. The entry file pulls in the libraries.

from openai import OpenAI
import streamlit as st

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= st.secrets["API_KEY"]
)

def chat_stream(history):
    stream = client.chat.completions.create(
        model="x-ai/grok-build-0.1",
        messages=history,
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content

#return -> 1 object ends.

###Yield -> generator. 
# Can return multiple times. each time it returns, it "pauses" and keeps its state. 
# When you call next() on it, it continues from where it left off until it hits the next yield.
# perfect when we want to stream data from API chunk by chunk instead of waiting for the whole response.