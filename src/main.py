import streamlit as st
from backend.sign_in import sign_in
import time

st.set_page_config(page_title="College Class Registration Portal", page_icon="🖥️", layout="wide")
st.title("College Class Registration Portal")

if 'session' not in st.session_state:
    st.session_state.session = 1 # This is just a placeholder
    st.session_state.AccountID = None
    st.session_state.StudentID = None
    st.session_state.rights = None

if not st.session_state.AccountID:

    st.header("Login In")

    email = st.text_input("Enter your school email address", placeholder="first.last@school.edu")
    password = st.text_input("Enter your password", type="password")

    if st.button("Login In"):
        if info := sign_in(email, password):
            st.session_state.AccountID = info[0]
            st.session_state.rights = info[1]
            st.write("Login Succesful")
            time.sleep(1)
            st.rerun()
        else:
            st.error("Invalid Email or Password!")



if st.session_state.AccountID and st.session_state.rights == "Student":
    st.write("Student Has Logged in!")

if st.session_state.AccountID and st.session_state.rights == "Admin":
    st.write("Admin Has Logged in!")


if st.session_state.AccountID:
    if st.button("Log Out!"):
        st.session_state.AccountID = None
        st.session_state.StudentID = None
        st.session_state.rights = None
        st.rerun()