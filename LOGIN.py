#----------IMPORTS
import mysql.connector
import streamlit as st
import hashlib

st.set_page_config(page_title="Client Query Management",layout="centered")
#--------SESSION STATE
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "role" not in st.session_state:
    st.session_state.role = ""
#----------DB CONNECTION/PASSWORD HASH/LOGIN FUNCTION
def db_connection():
    connector = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="client_query_db"
    )
    cursor = connector.cursor()
    return connector,cursor

def get_hashpwd(pwd):
     return hashlib.sha256(pwd.encode()).hexdigest()

def login_user(username,password,role):
    conn,cur = db_connection()
    login_hash_pwd = get_hashpwd(password)
    cur.execute("SELECT * FROM users WHERE username=%s AND hashed_password=%s and role=%s",(username,login_hash_pwd,role))
    result=cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return True
    else:
        return False
    
#-------------------STREAMLIT UI
st.title("Client Query Management")
st.subheader("Login")
username = st.text_input("Enter Username")
password = st.text_input("Password", type="password")
role = st.radio("Client/Support", ['Client', 'Support'],horizontal=True)
login_clicked = st.button("Login",type="secondary")

if login_clicked:
        if not username or not password:
            st.error("Username and password cannot be empty")
        else:
            status=login_user(username,password,role)
            if status:
                st.success("Login sucessful")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                if role == "Client":
                   st.switch_page("pages/Client_Dashboard.py")
                else:
                   st.switch_page("pages/Support_Dashboard.py")
            else:
                st.error("Invalid Credentials")