import streamlit as st
from streamlit_chat import message
from PIL import Image
from query.vortex_query import VortexQuery


def initialize_page():
    st.set_page_config(page_title='ChatCCNL', page_icon=':books:')
    st.image(logo_image, width=500)
    st.header("ChatCCNL")
    st.markdown("[Scarica i CCNL dal sito di Cifa Italia](https://www.cifaitalia.it/cifa-cosa-facciamo/ccnl.html)")


def handle_query_form():
    with st.form(key='query_form'):
        user_query = st.text_input('Domanda: ', '', key='input',
                                   help='Chiedimi informazioni sui CCNL di CIFA Italia?')
        submit_button = st.form_submit_button('Invia')
    return user_query, submit_button


def display_chat_history():
    for i, (user_msg, ai_msg) in enumerate(zip(st.session_state['past'][::-1],
                                               st.session_state['generated'][::-1])):
        message(user_msg, is_user=True, key=f"user_{i}")
        message(ai_msg, key=f"ai_{i}")


def query(question: str) -> str:
    """
    Query the VortexQuery model with the provided question
    :param question: The question to ask the model
    :return: The answer from the model
    """
    vortex_query = VortexQuery()
    answer, _ = vortex_query.ask_question(question)
    return answer


logo_image = Image.open('logo.png')

# Initialize page and session state
st.session_state.setdefault('generated', [])
st.session_state.setdefault('past', [])

initialize_page()
user_query, submit_button = handle_query_form()

if submit_button and user_query:
    model_response = query(user_query)
    st.session_state.past.append(user_query)
    st.session_state.generated.append(model_response)

display_chat_history()
