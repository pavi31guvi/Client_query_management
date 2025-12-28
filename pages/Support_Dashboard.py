#-------------IMPORTS
import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in :
    st.error("Please login first")
    st.stop()

if st.session_state.role != "Support":
    st.error("Permit allowed for Support Users Only.")
    st.stop()

if "show_queries" not in st.session_state:
        st.session_state.show_queries = False

# ------------FUNC: DB CONNECTION/FILTER QUERIES BY STATUS FUNCTION
def db_connection():
    connector = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="client_query_db"
    )
    cursor = connector.cursor(dictionary=True)
    return connector, cursor

def fetch_queries(status):
    conn, cur = db_connection()
    if status == "Open":
        cur.execute("SELECT * FROM queries WHERE status = 'Open' ORDER BY date_raised DESC ;")
    elif status == "Closed":
        cur.execute("SELECT * FROM queries WHERE status = 'Closed' ORDER BY date_raised DESC ;")
    else:
        cur.execute("SELECT * FROM queries;")
    result = cur.fetchall()
    data=pd.DataFrame(result)
    cur.close()
    conn.close()
    return data

# ---------------- CLOSE SELECTED QUERIES ----------------
def close_queries(query_ids):
    conn, cur = db_connection()
    for qid in query_ids:
        cur.execute("""
            UPDATE queries
            SET status = 'Closed',date_closed = %s
            WHERE query_id = %s And status = 'Open';
        """, (datetime.now(), qid))
    conn.commit()
    cur.close()
    conn.close()

#--------------DF FORMATTER-------------
def format_dataframe(df):
    if df.empty:
        return df
    else:
        df["Query Code"] = df["query_id"].apply(lambda x: f"Q{x:04d}")
        df = df.drop(columns=["query_id"])
        cols = list(df.columns)
        cols.remove("Query Code") 
        cols.insert(0, "Query Code")
    return df[cols]

# ---------------- STREAMLIT UI ----------------
if st.session_state.logged_in and st.session_state.role == "Support":
    st.title("Client Query Management")
    st.subheader(f"Welcome {st.session_state.username} , Support Dashboard")
    selected_status = st.selectbox("Filter Queries", ['Open','Closed','All'])

    # Reset show_queries when dropdown changes
    if "last_status" not in st.session_state:
        st.session_state.last_status = selected_status

    if selected_status != st.session_state.last_status:
        st.session_state.show_queries = False
        st.session_state.last_status = selected_status

    submit = st.button("Submit")
    if submit:
        st.session_state.show_queries = True

    if  st.session_state.show_queries:    
        df = fetch_queries(selected_status)
        if selected_status == "Open":
            if df.empty:
                st.info("No Open queries available")
            else:
                opened_query_ids = df['query_id'].tolist()
                id_map = {f"Q{x:04d}": x for x in opened_query_ids} 
                select_all_ids = st.checkbox("Select all query_id to close")
                if select_all_ids:
                    selected_ids = opened_query_ids
                else:
                    selected_display = st.multiselect("Select Query Id", list(id_map.keys()))
                    selected_ids = [id_map[d] for d in selected_display]  

                if selected_ids:
                    st.dataframe(df[df["query_id"].isin(selected_ids)])

                closed_clicked = st.button("Close Query")     
                if closed_clicked:
                    if not selected_ids :
                        st.warning("At least one query id should be selected")
                    else:
                        close_queries(selected_ids)
                        conn, cur = db_connection()
                        #---------AFTER CLOSING
                        placeholders = ",".join(["%s"]*len(selected_ids))
                        sql = f"select * from queries where query_id in ({placeholders})"
                        cur.execute(sql,tuple(selected_ids))
                        After_closing = cur.fetchall()
                        cur.close()
                        conn.close()
                        df_opened=pd.DataFrame(After_closing)
                        df_opened= format_dataframe(df_opened)
                        st.dataframe(df_opened)
                        st.success("Closed the query sucessfully")
        elif selected_status =='Closed':
            if df.empty:
                st.info("No Closed queries available")
            else:              
                df_closed= pd.DataFrame(df)
                df_closed = format_dataframe(df_closed)
                st.dataframe(df_closed)
        else:
            if df.empty:
                st.info("No data or rows found")
            else: 
                df_all= pd.DataFrame(df)
                df_all = format_dataframe(df_all)
                st.dataframe(df_all)

    logout = st.button("Logout")
    if logout:
        st.session_state.show_queries = False
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.email_id = None
        st.session_state.username  = None
        st.success("You have logged out sucessfully")
        st.switch_page("LOGIN.py")