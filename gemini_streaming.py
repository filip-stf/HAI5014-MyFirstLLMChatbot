import os
import streamlit as st
from openai import OpenAI
import time

# Set page configuration
st.set_page_config(
    page_title="Gemini Chatbot",
    page_icon="💬",
    layout="wide"
)

# Initialize OpenAI client
@st.cache_resource
def get_client():
    token = os.environ["GOOGLE_API_KEY"]
    endpoint = "https://generativelanguage.googleapis.com/v1beta/openai/"
    return OpenAI(
        base_url=endpoint,
        api_key=token,
    )

client = get_client()
model_name = "gemini-2.0-flash"

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display title
st.title("💬 Gemini Chatbot")
st.markdown("Chat with Gemini using streaming responses.")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't display system messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Get user input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat and state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message in chat
    with st.chat_message("user"):
        st.write(user_input)

    # Display assistant response with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Create a container for usage info
        usage_container = st.container()
        
        try:
            # Get streaming response from the model
            response = client.chat.completions.create(
                messages=st.session_state.messages,
                model=model_name,
                stream=True,
                stream_options={'include_usage': True}
            )
            
            usage = None
            
            # Process the streaming response
            for update in response:
                if update.choices and update.choices[0].delta:
                    content = update.choices[0].delta.content or ""
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")
                    time.sleep(0.01)  # Small delay for smoother appearance
                
                if update.usage:
                    usage = update.usage
            
            # Display the final response without cursor
            message_placeholder.markdown(full_response)
            
            # Store the assistant's reply in the conversation history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Display usage information if available
            if usage:
                with usage_container:
                    with st.expander("API Usage Details"):
                        for k, v in usage.dict().items():
                            st.text(f"{k} = {v}")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            full_response = f"I encountered an error: {str(e)}"
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add a button to clear the chat history
if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
    st.rerun()

# Display information in the sidebar
with st.sidebar:
    st.title("About")
    st.markdown("""
    This chatbot uses Google's Gemini model through the OpenAI-compatible API.
    
    - Type your message in the input box
    - The assistant will respond in real-time
    - Conversation history is maintained during your session
    - API usage details are shown beneath each response
    """)