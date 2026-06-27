# knows how to draw the web page. 
# Each file = one job. When something breaks, you know which file to open.
import streamlit as st
from backend import chat_stream
from database import log_in, sign_up, log_out, save_message, load_messages, clear_messages


st.set_page_config(page_title="Calvin's AI", page_icon="🚀")


# --- 1. USER LOGIN / SIGN UP GUARD ---
# If the user is not logged in yet, we show the Login screen and STOP the app here.
if "user" not in st.session_state:
    st.title("My First AI App!😃")
    st.subheader("Please Log In or Sign Up to start talking to your AI!")

    tab1, tab2 = st.tabs(["🔑 Log In", "📝 Sign Up"])

    with tab1:
        email = st.text_input("Email Address", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Log In"):
            user, error_message = log_in(email, password)
            if error_message:
                st.error(error_message)
            else:
                st.session_state.user = user
                st.success("Successfully logged in! 🎉")
                st.rerun()

    with tab2:
        new_email = st.text_input("New Email Address", key="signup_email")
        new_password = st.text_input("New Password", type="password", key="signup_password")
        if st.button("Create Account"):
            user, error_message = sign_up(new_email, new_password)
            if error_message:
                st.error(error_message)
            else:
                st.success("Account created successfully! Now go to the Log In tab. 🎉")
                
    st.stop() # Stops Streamlit from running any code below if user is not logged in!


# --- 2. MAIN CHAT APPLICATION (Runs only when logged in) ---
user_id = st.session_state.user.id
user_email = st.session_state.user.email

st.title("My First AI App!😃")


# Sidebar - Clear Chats, Different Chats, Log Out
with st.sidebar:
    st.header("Settings")
    st.write(f"Logged in as: **{user_email}**")
    
    current_chat = st.radio("Pick a Room", ["Helpful Tutor", "Sarcastic Robot", "Pirate"])
    
    # Clear Chat Button
    if st.button("Clear Chat"):
        clear_messages(user_id, current_chat) # Delete from Supabase database
        st.session_state[current_chat] = []   # Clear in our active session memory
        st.rerun()

    # Log Out Button
    if st.button("Log Out"):
        log_out()
        del st.session_state.user
        # Clean up session memory so the next user doesn't see our old chats
        for room in ["Helpful Tutor", "Sarcastic Robot", "Pirate"]:
            if room in st.session_state:
                del st.session_state[room]
        st.rerun()


# Setup the specific room's memory if it doesn't exist in active session
if current_chat not in st.session_state:
    # Load all past chat history from Supabase database!
    db_messages = load_messages(user_id, current_chat)
    
    if len(db_messages) == 0:
        # If there are no past messages, add the starting character prompt
        st.session_state[current_chat] = [
            {"role": "system", "content": f"You are a {current_chat}. Stay in character!"}
        ]
    else:
        # Otherwise, load our saved messages!
        st.session_state[current_chat] = db_messages


# Display past messages
for messages in st.session_state[current_chat]:
    if messages["role"] == "system":
        continue
    with st.chat_message(messages["role"]):
        st.write(messages["content"])


# Input box for user prompt
prompt = st.chat_input("Say something")
if prompt:
    # Show user message in UI
    with st.chat_message("user"):
         st.write(prompt)
     
    # Save user message in local memory AND Supabase!
    st.session_state[current_chat].append({"role": "user", "content": prompt})
    save_message(user_id, current_chat, "user", prompt)

    # Generate and stream response from AI
    with st.chat_message("assistant"):
        response = st.write_stream(chat_stream(st.session_state[current_chat]))

    # Save AI response in local memory AND Supabase!
    st.session_state[current_chat].append({"role": "assistant", "content": response})
    save_message(user_id, current_chat, "assistant", response)


# List of Streamlit Functions: https://docs.streamlit.io/library/api-reference
