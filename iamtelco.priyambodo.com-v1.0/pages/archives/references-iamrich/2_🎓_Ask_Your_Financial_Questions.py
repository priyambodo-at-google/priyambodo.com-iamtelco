import streamlit as st
import call_gemini as genai
import time

st.set_page_config(page_icon="image/usd.ico")

def show_progress():
    with st.spinner('Please wait for my answer...'):
        time.sleep(5)

vNoLabel = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(vNoLabel, unsafe_allow_html=True)

def clear_chat():
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi..., I am a Financial Advisor and Wealth Manager, very knowledgeable about financial industry especially investing in stock market. How can I help you? (ex: Who are you? What are the top 10 best stocks to buy today? How can I be rich?)"}]

st.title("💬 Ask your Financial Questions")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hi..., I am a Financial Advisor and Wealth Manager, very knowledgeable about financial industry especially investing in stock market. How can I help you? (ex: Who are you? What are the top 10 best stocks to buy today? How can I be rich?)"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    context = "Act as a Financial Advisor, your name is IamRich. "
    context += "You are an Investment Expert and Wealth Manager consultant, very knowledgeable about financial industry especially investing in stock market. "
    context += "Please answer this question: "
    prompt = context + prompt
    show_progress()
    try:
        response = genai.genai_gemini_text_nolongchain(prompt)
        #st.info(response)
    except Exception as e:
        st.error(e)
        st.warning(f"Sorry there are no results available for this question, please ask another question.")

    msg = {"role": "assistant", "content": response}
    st.session_state.messages.append(msg)
    st.chat_message("assistant").markdown(msg["content"])

if len(st.session_state.messages) > 1:
    st.button('Clear Chat', on_click=clear_chat)