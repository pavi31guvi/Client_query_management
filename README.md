# Client_query_management System

A **Streamlit + MySQL** based application for managing client queries.  
This project provides role-based dashboards for **Clients** and **Support users**, with secure login, query submission, query tracking, and query resolution.

---

## Features
- **Role-based access**
  - Clients can submit queries and track their status.
  - Support users can filter, view, and close queries.
- **Secure login**
  - Passwords stored as SHA-256 hashes.
  - Session state ensures secure access and logout.
- **Query management**
  - Clients submit queries with email, mobile, heading, and description.
  - Support users filter queries by status (`Open`, `Closed`, `All`) and close them.
- **Session handling**
  - Prevents unauthorized access.
  - Clean logout flow.

---

## Tech Stack
- **Frontend/UI**: Streamlit
- **Database**: MySQL
- **Backend/Logic**: Python (`mysql.connector`, `pandas`)

---

## 📂 Project Structure
```
│── db_setup.py                  # Database setup and initial data import
│── login.py                      # Login page
│── pages/
│    ├── Client_Dashboard.py     # Client dashboard
│    └── Support_Dashboard.py    # Support dashboard
│── users_table.csv              # data for users
│── synthetic_client_queries.csv # data for queries
│── screenshots/                 # Screenshots of the app
│── README.md                     # Documentation
```

---

## Setup & Usage

### 1. Clone the repository
```bash
git clone https://github.com/pavi31guvi/Client_query_management.git
cd client-query-management
```
### 2. Install dependency
```bash
!pip3 install pandas
!pip3 install streamlit
!pip3 install mysql-connector-python
```
### 3. Initialize the database
```bash
python db_setup.py
```
This will:
 - Create the database client_query_db.
 - Create users and queries tables.
 - Import data from users_table.csv and synthetic_client_queries.csv.

### 4. Run the streamlit app
```bash
streamlit run login.py
```
- **Login (login.py)**
 - Provides login form with username, password, and role (Client or Support).
 - Validates credentials against the users table.
 - Redirects to the appropriate dashboard:
     - Client_Dashboard.py for clients.
     - Support_Dashboard.py for support users.
- **Client Dashboard (Client_Dashboard.py)**
 - Allows clients to:
     - Submit new queries.
     - View the status of their queries.
     - Validates email and mobile number.
     - Displays queries with formatted IDs and status.
     - Logout clears session state and redirects to login.
- **Support Dashboard (Support_Dashboard.py)**
 - Allows support users to:
     - Filter queries by status (Open, Closed, All).
     - Select and close queries.
     - View updated query status immediately.
     - Logout clears session state and redirects to login.
  
