# Knows how to talk to Supabase. database.py is never run directly. It's a library.
# This file does one job: Handles database storage and user accounts!

from supabase import create_client
import streamlit as st

# 1. Connect to our Supabase database using secrets (our special keys)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# --- ACCOUNT FUNCTIONS (Authentication) ---

# Create a brand new user account
def sign_up(email, password):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        return response.user, None
    except Exception as e:
        return None, str(e)


# Log in to an existing account
def log_in(email, password):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        return response.user, None
    except Exception as e:
        return None, str(e)


# Log out of the account
def log_out():
    try:
        supabase.auth.sign_out()
    except Exception as e:
        pass


# --- CHAT HISTORY FUNCTIONS (Memory) ---

# Save a single message to Supabase so we remember it forever!
def save_message(user_id, room, role, content):
    try:
        supabase.table("chat_history").insert({
            "user_id": user_id,
            "room": room,
            "role": role,
            "content": content
        }).execute()
    except Exception as e:
        st.error(f"Could not save message to database: {e}")


# Load all past messages for a specific room
def load_messages(user_id, room):
    try:
        response = supabase.table("chat_history") \
            .select("role", "content") \
            .eq("user_id", user_id) \
            .eq("room", room) \
            .order("created_at", desc=False) \
            .execute()
        return response.data
    except Exception as e:
        st.error(f"Could not load messages from database: {e}")
        return []


# Delete all messages for a specific room (clear chat memory)
def clear_messages(user_id, room):
    try:
        supabase.table("chat_history") \
            .delete() \
            .eq("user_id", user_id) \
            .eq("room", room) \
            .execute()
    except Exception as e:
        st.error(f"Could not clear messages: {e}")
