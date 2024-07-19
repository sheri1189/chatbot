import streamlit as st
from langchain.chat_models import ChatOpenAI
from streamlit_chat import message
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from itertools import zip_longest
openapi_key = st.secrets['OPENAI_API_KEY']
st.set_page_config(page_title="Ibexstack Chatbot")
st.markdown(
    """
    <h1 style='font-size:30px;'>Ibexstack Conversational AI (CHATGPT-TYPE)</h1>
    """,
    unsafe_allow_html=True
)
if "generated" not in st.session_state:
    st.session_state["generated"] = []
if "past" not in st.session_state:
    st.session_state["past"] = []
if "entered_prompt" not in st.session_state:
    st.session_state["entered_prompt"] = ""
chat = ChatOpenAI(
    temperature=0.5,
    model="gpt-3.5-turbo",
    openai_api_key=openapi_key,
    max_tokens=40,
)


def build_message_list():
    """
    Build a list of messages including system, human, and AI messages.
    """
    zipped_messages = [
        SystemMessage(
            content="""
            Your name is AI Mentor. You are an AI Technical Expert for Artificial Intelligence. Ask the user about their name before starting, and you are here to guide and assist students with their AI-related questions.
            1. Greet the user politely, ask their name, and inquire how you can assist them with AI-related queries.
            2. Provide informative and relevant responses to questions about artificial intelligence, machine learning, and deep learning.
            3. Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discussion that may be inappropriate.
            4. If the user asks about a topic unrelated to AI, politely steer the conversation back to AI or inform them that you are here to assist with AI-related queries.
            5. Be patient and considerate when responding to user queries, and provide clear explanations.
            6. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
            7. Do not generate long paragraphs in response. Maximum words should be 100.
            Remember, your primary goal is to assist and educate students in the field of Artificial Intelligence. Always provide helpful and accurate information.
            """
        )
    ]
    for human_message, ai_message in zip_longest(st.session_state["past"], st.session_state["generated"]):
        if human_message is not None:
            zipped_messages.append(HumanMessage(content=human_message))
        if ai_message is not None:
            zipped_messages.append(AIMessage(content=ai_message))
    return zipped_messages


def generate_response():
    """
    Generate AI response by using the ChatOpenAI Model.
    """
    zipped_messages = build_message_list()
    ai_response = chat(zipped_messages)
    return ai_response


def submit():
    st.session_state.entered_prompt = st.session_state.prompt_input
    st.session_state.prompt_input = ""


st.text_input("What's your query?", key="prompt_input", on_change=submit, placeholder="Type your query here")
if st.session_state.entered_prompt != "":
    user_query = st.session_state.entered_prompt
    st.session_state.past.append(user_query)
    output = generate_response()
    st.session_state.generated.append(output.content)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['past'][i], is_user=True, key=str(i)+'_user')
        message(st.session_state['generated'][i], key=str(i))
