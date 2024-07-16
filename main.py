import streamlit as st
import anthropic

st.title("Chatbot con Sonnet 3.5")

client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key= st.secrets["ANTHROPIC_API_KEY"]
)

if "model" not in st.session_state:
    st.session_state["model"] = "claude-3-5-sonnet-20240620"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Mensaje a Claude...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        with client.messages.stream(
            max_tokens=1024,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            model=st.session_state["model"],
        ) as stream:
            for text in stream.text_stream:
                if text is not None:
                    full_response += text
                    message_placeholder.markdown(full_response + "▌")