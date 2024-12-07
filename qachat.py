from dotenv import load_dotenv
load_dotenv() ## loads all the environmental variables

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load Gemini Pro Model and get responses
model=genai.GenerativeModel("gemini-pro")

chat=model.start_chat(history=[])

def get_gemini_response(question, history):
    #construct a new prompt incorporating relevant history
    prompt= f"""You are an AI expert psychologist who knows Beck's  Cognitive theory very well.
There are 3 important parameters in the Beck's Cognitive Theory to understand the Depression.
1. Cognitive Traid  2.Negative Self Schema 3.Faulty Information Processing.
You need to act like a conversational AI agent who is psychologist to ask questions to
the user to identify the cognitive traid mechanisms in user.

You need to think logically as below:
1.You need to consider previous historic conversation provided.
2.You need to ask questions to get the views about the cognitive traid parameters in user;
cognitive traid parameters include i.negativity towards self ii.negativity towards future iii.negativity
towards world(friends, family, colleagues, relatives, teachers etc.)
Ask the questions indirectly do not explicitly say about you are asking information about cognitive traid.
3.Strictly ask questions about the parameter one at a time. Do not ask at once about all
the cognitive triad parameters at once, it should be like couselling.
Ask about only one cognitive traid parameter at once. Do not ask too much in one question.
4.You are concentrating on only cognitive traid parameter, not on negative self schema
and fault information processing.
5.You first message in the conversation is already provided to the user like "Hello,
Greetings of the day.".
Strictly do not wish again like "hello","hi", etc. Come to the point directly.
6.To get the information of the user about cognitive traid mechanisms, ask the relevant
information fromt the user wherever required. So if user's first message is  Greetings,
then do not reply with greetings again, you can start fetching information about cognitive traid.
7.You question should be crisp. Question should not be lengthy.
    
    Here's the conversation so far : \n\n
    {' '.join([f'{role}: {text}' for role, text in history])} \n\n
    Now, here's the user's new query: {question} \n\n
    Please provide a comprehensive and informative response."""

    response=chat.send_message(prompt, stream=False)
    #stream=false content is generate all at once
    return response

##initiate our streamlit app
st.set_page_config(page_title="Chatbot Demo")

st.header("Gemini LLM Chatbot Application")

##Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[("Bot","Hello,Greetings of the day.")]

input=st.text_input("Input: ", key="input")
submit=st.button("Ask the Question")

if submit and input:
    response=get_gemini_response(input, st.session_state['chat_history'])
    #Add user query and response to session state chat history
    st.session_state['chat_history'].append(("User", input))
    #for chunk in response:
        #st.session_state['chat_history'].append(("Bot", chunk.text))

    response_filter=response.candidates[0].content.parts
    response_text=' '.join(part.text for part in response_filter)
    st.session_state['chat_history'].append(("Bot", response_text))
st.subheader("The Chat History")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")