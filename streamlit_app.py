import streamlit as st
from services.chat_service import ChatService

# Set page config
st.set_page_config(
    page_title="DeepSeek V3 Chatbot",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def local_css():
    st.markdown("""
    <style>
    .stTextInput {
        width: 100%;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .chat-message.assistant {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .chat-message .message-content {
        display: flex;
        margin-bottom: 0.5rem;
    }
    .chat-message .message-content img {
        width: 42px;
        height: 42px;
        border-radius: 0.5rem;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message-content .message-text {
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        flex-grow: 1;
    }
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    local_css()
    st.title("DeepSeek V3 Chatbot")
    
    # Initialize chat service
    if 'chat_service' not in st.session_state:
        st.session_state.chat_service = ChatService()
    
    # Initialize chat history
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            response = st.session_state.chat_service.generate_response(prompt)
            st.markdown(response)
            
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()
