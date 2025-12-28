#---------------IMPORTS
import pandas as pd
import mysql.connector
import hashlib

#---------DB CONNECTION
connector = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789"
)
cursor = connector.cursor()

cursor.execute("""DROP DATABASE IF EXISTS client_query_db""")
cursor.execute("""Create database client_query_db""")

connector = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456789",
    database="client_query_db"
)
cursor = connector.cursor()

#----------PASSWORD HASH
def get_hashpwd(pwd):
     return hashlib.sha256(pwd.encode()).hexdigest()

#-----------TABLE CREATION/INSERTION

user_table = """CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    role VARCHAR(50) NOT NULL,
    user_email VARCHAR(255) UNIQUE NOT NULL
);"""
cursor.execute(user_table)

queries_table = """CREATE TABLE IF NOT EXISTS queries (
    query_id INT AUTO_INCREMENT PRIMARY KEY, 
    client_email VARCHAR(100) NOT NULL,
    client_mobile VARCHAR(15) NOT NULL,
    query_heading VARCHAR(200) NOT NULL,
    query_description TEXT NOT NULL,
    status VARCHAR(10) NOT NULL,
    date_raised DATETIME NOT NULL,
    date_closed DATETIME NULL
);"""
cursor.execute(queries_table)

#--------IMPORTS CSV FILE TO USERS TABLE
path = r"C:\Users\91770\Documents\Data Science\Zen DS Day 1 Sept 27\CDB\users_table.csv"
df = pd.read_csv(path)
df = df.where(pd.notnull(df), None)
df_users =[]

insert_users="""Insert into users(username,hashed_password,role,user_email)
 values (%s,%s,%s,%s)"""

for index,row in df.iterrows():
    df_users.append((
    row["username"],
    get_hashpwd(row["password"]),
    row["role"],
    row["user_email"]
    ))

cursor.executemany(insert_users,df_users)
connector.commit()

print("Imported the users data successfully")

#--------IMPORTS CSV FILE TO QUERIES TABLE
path = r"C:\Users\91770\Documents\Data Science\Zen DS Day 1 Sept 27\CDB\synthetic_client_queries.csv"
df = pd.read_csv(path)
df = df.where(pd.notnull(df), None)
data =[]

insert_queries="""Insert into queries(client_email,client_mobile,query_heading,query_description,
status,date_raised,date_closed) values (%s,%s,%s,%s,%s,%s,%s)"""

#Convert date columns:
df['date_raised'] = pd.to_datetime(df['date_raised'],format="%d-%m-%Y")
df['date_closed'] = pd.to_datetime(df['date_closed'],format="%d-%m-%Y")

for index,row in df.iterrows():
    data.append((
    row["client_email"],
    row["client_mobile"],
    row["query_heading"],
    row["query_description"],
    row["status"],
    row["date_raised"],
    row["date_closed"]
    ))

cursor.executemany(insert_queries,data)
connector.commit()

print("Imported the Queries data successfully")