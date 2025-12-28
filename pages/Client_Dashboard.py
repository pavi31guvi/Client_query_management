#-------------IMPORTS
import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

#-------------LOGIN PROTECTION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.error("Please login first")
    st.stop()

if st.session_state.role != "Client":
    st.error("This Page is for client Users Only.")
    
#-----------FUNC : DB CONNECTION/CLIENT QUERY INSERTION & QUERY STATUS TRACKING
def db_connection():
    connector = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="client_query_db"
    )
    cursor = connector.cursor()
    return connector,cursor

def submit_query(mail, mobile, heading, description):
    conn,cur = db_connection()
    submit_sql="""INSERT INTO queries (client_email, client_mobile, query_heading, query_description,status,date_raised)
    VALUES (%s, %s, %s, %s, %s, %s)"""
    values=(mail,mobile,heading,description,"Open",datetime.now())
    cur.execute(submit_sql,values)
    conn.commit()
    cur.close()
    conn.close()
    return True

def validate_user_email(username,email):
    conn,cur = db_connection()
    email_sql = "select user_email from users where username=%s"
    cur.execute(email_sql,(username,))
    email_data = cur.fetchone()
    cur.close()
    conn.close()
    if email_data and email_data[0]== email:
        return True
    return False

def fetch_client_status():
     conn,cur = db_connection()
     fetch_sql = """ select query_id,query_heading, query_description, status, date_raised, date_closed 
     FROM queries WHERE client_email = %s ORDER BY date_raised DESC """
     cur.execute(fetch_sql,(st.session_state.email_id,))
     fetch_data = cur.fetchall()
     cur.close()
     conn.close()
     return fetch_data

#---------------STREAMLIT CLIENT UI
if st.session_state.logged_in and st.session_state.role == "Client":

    st.title("Client Query Management")
    st.subheader(f"Welcome {st.session_state.username} , Client Dashboard")
    st.text(" ")

    email_id = st.text_input("Email id")
    Mobile_Number = st.text_input("Mobile Number")
    Query_Heading = st.text_input("Query Heading")
    Query_Description = st.text_input("Query Description")
    st.session_state.email_id = email_id
    submit=st.button("Submit")

    if submit:
        if not email_id or not Mobile_Number or not Query_Heading or not Query_Description:
            st.error("All fields are required")
        elif '@' not in st.session_state.email_id or '.' not in st.session_state.email_id:
            st.error("Enter a valid email address")
        elif not Mobile_Number.isdigit():
            st.error("Mobile number should contains only digits")   
        elif len(Mobile_Number) != 10:
            st.error("Mobile Number should be exactly 10 digits 0-9")
        elif not validate_user_email(st.session_state.username, st.session_state.email_id):
            st.error("The email does not match your logged-in account. Please use your registered email.")
        else:
            result=submit_query(st.session_state.email_id,Mobile_Number,Query_Heading,Query_Description)
            if result:
                st.success("Query Submitted Sucessfully.Kindly wait our Support team will contact you.")
#----------------QUERY STATUS TRACKING
    view_clicked= st.button("View my Queries")
    if view_clicked:
        if not st.session_state.email_id:
            st.warning("Please enter your email to view your queries.")
        elif '@' not in st.session_state.email_id or '.' not in st.session_state.email_id:
            st.error("Enter a valid email address")
        elif not validate_user_email(st.session_state.username, st.session_state.email_id):
            st.error("The email does not match your logged-in account. Please use your registered email.")
        else:
            my_queries_data = fetch_client_status() 
            formatted_data = []
            if not my_queries_data:
                st.info("No Queries Submitted yet") 
            else:
                for qry in my_queries_data:
                    query_id=qry[0]
                    display_code = f"Q{query_id:04d}"
                    formatted_data.append({
                        "Query Id" : display_code,"Query Heading" : qry[1],"Query Description" : qry[2],
                        "Query status" : qry[3], "Query Created time" : qry[4].strftime("%d-%m-%Y"),
                        "Query Closed_time" : qry[5].strftime("%d-%m-%Y") if qry[5] else "Not Closed Yet"
                    })
            if formatted_data:
                df = pd.DataFrame(formatted_data)
                st.dataframe(df)
    
    logout = st.button("Logout")
    if logout:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.email_id = None
        st.session_state.username  = None
        st.success("You have logged out sucessfully")
        st.switch_page("LOGIN.py")