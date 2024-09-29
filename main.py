import streamlit as st
from backend import interpret_command_with_gpt, process_interpreted_command, writeAssistantResponse, retrieveDataFromDatabase, addDataToDatabase

# Initialize session state for messages, chatbot visibility, and context
if "messages" not in st.session_state:
    st.session_state.messages = []
if "show_chatbot" not in st.session_state:
    st.session_state.show_chatbot = False
if "context" not in st.session_state:
    st.session_state.context = ""  # Initialize context to store conversation history

# Title of the app
st.title("Example Chatbot using Gemini API")

# Button to start chatting with the bot
if st.button("Start Chatting"):
    st.session_state.show_chatbot = True
    history = retrieveDataFromDatabase()
    for chat in history:
        st.session_state.messages.append({"role": "user", "content": chat["user"]})
        st.session_state.messages.append({"role": "assistant", "content": chat["bot"]})

    # Initial message from the assistant when chat starts
    response = "Hi there, How can I assist you?"
    st.session_state.context += f"Bot: {response}\n"  # Add response to the context

# Display the chatbot interface once the chat starts
if st.session_state.show_chatbot:
    # Display each message from the session state
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User prompt input
    if prompt := st.chat_input("What is up?"):
        # Display the user input in the chat window
        with st.chat_message("user"):
            st.markdown(f"You: {prompt}")
        # Save user input to session state
        st.session_state.messages.append({"role": "user", "content": f"You: {prompt}"})
        
        # Append user input to context
        st.session_state.context += f"User: {prompt}\n"
        
        # Interpret the command with GPT, passing the full conversation context
        full_prompt = f"Previous chat context: {st.session_state.context}\n\nCurrent message: {prompt}"
        interpreted_command = interpret_command_with_gpt(full_prompt)
        
        # Process the interpreted command (generates response)
        response = process_interpreted_command(interpreted_command)
        
        # Append assistant's response to context
        st.session_state.context += f"Bot: {response}\n"
        
        # Display the assistant's response with typing animation
        if "code" in response:  # Simple heuristic to detect code-related output
            with st.chat_message("A"):
                a = response["language"]
                st.code(response, language= "python")  # Display response as a Python code block
        else:
            # Display the assistant's response with typing animation
            addDataToDatabase(prompt, response)
            writeAssistantResponse(response) 
            
        
