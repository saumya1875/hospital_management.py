import streamlit as st
import mysql.connector
import bcrypt
import pandas as pd
import base64

## CSS to hide Streamlit Cloud elements
hide_streamlit_cloud_elements = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    a[title="View source"] {display: none !important;}
    button[kind="icon"] {display: none !important;}
    </style>
"""
st.markdown(hide_streamlit_cloud_elements, unsafe_allow_html=True)
    

# Background styling
def set_bg_from_local(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.3)),
            url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            font-weight: bold !important;
            padding: 20px;
            margin: 5px;
        }}
        
        .stButton > button {{
            background-color: blue;
            color: white;
            padding: 12px 24px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }}
        .stButton > button:hover {{
            background-color: #45a049;
        }}
        .stTextInput > div > div > input, .stTextArea > div > div > textarea {{
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            border: 1px solid black;
        }}
        label {{
            font-weight: bold;
            color: green;
             font-size: 16px;
        }}
        .stSelectbox > div > div > select {{
            padding: 10px;
            margin: 5px;
            border-radius: 5px;
            border: 1px solid #ccc;
        }}
        .stDataFrame {{
            background-color: lightblue;
            padding: 10px;
            border-radius: 20px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            # font-size:50px;
            
        }}
        
        .stSubheader {{
            font-size: 50px;
            color: #333;
            padding: 0px;
            background-color: blue;
            border-radius: 5px;
            margin-bottom: 15px;
            font-style:bold;
            
        }}
        
    
        </style>
    """, unsafe_allow_html=True)

# Database connection
def connect_to_mysql():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='hospital_management'
        )
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# User registration
def register_user(username, password, role):
    conn = connect_to_mysql()
    if conn:
        cursor = conn.cursor()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                       (username, hashed_password, role))
        conn.commit()
        cursor.close()
        conn.close()

# User authentication
def authenticate_user(username, password):
    conn = connect_to_mysql()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, password, role FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.fetchall()
        cursor.close()
        conn.close()
        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            return True, user[2], user[0]
    return False, None, None

# Doctor operations
def add_doctor(name, specialty):
    conn = connect_to_mysql()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO doctors (name, specialty) VALUES (%s, %s)", (name, specialty))
        conn.commit()
        cursor.close()
        conn.close()

def get_doctors():
    conn = connect_to_mysql()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, specialty FROM doctors")
        doctors = cursor.fetchall()
        cursor.close()
        conn.close()
        return doctors
    return []

# Patient operations
def add_patient(name, age, gender, address, doctor_id=None):
    conn = connect_to_mysql()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO patients (name, age, gender, address, doctor_id) VALUES (%s, %s, %s, %s, %s)",
                       (name, age, gender, address, doctor_id))
        conn.commit()
        cursor.close()
        conn.close()

def view_patients():
    conn = connect_to_mysql()
    if conn is None:
        return pd.DataFrame()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id, p.name, p.age, p.gender, d.name AS doctor_name, d.specialty 
        FROM patients p 
        LEFT JOIN doctors d ON p.doctor_id = d.id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=["ID", "Name", "Age", "Gender", "Doctor Name", "Doctor Specialty"])

# Main app logic
def main():
    # set_bg_from_local("sa.jpg")
    st.title("🏥 Hospital Management System")

    # Initialize session state
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.user_id = None
        
        

    # Menu
    menu = ["Login", "Register", "Add Doctor", "Add Patient", "View Patients", "Logout"]
    choice = st.sidebar.selectbox("Select Action", menu)

# Set background dynamically based on menu choice
    background_images = {
        "Login": "sa.jpg",
        "Register": "mmm.jpg",
        "Add Doctor": "mmmm.jpg",
        "Add Patient": "as.jpg",
        "View Patients": "a1.jpg",
        "Logout": "sa.jpg"
    }
    set_bg_from_local(background_images.get(choice, "sa.jpg"))
    
    if choice == "Login":
        # set_bg_from_local("sa.jpg")
        st.subheader("🔐 Login to your account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            authenticated, role, user_id = authenticate_user(username, password)
            if authenticated:
                st.session_state.logged_in = True
                st.session_state.role = role
                st.session_state.user_id = user_id
                st.success(f"Welcome, {username} ({role})!")
            else:
                st.error("Invalid username or password")

    elif choice == "Register":
        # set_bg_from_local("mmm.jpg")
        st.subheader("📝 Create a new account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        role = st.selectbox("Role", ["admin", "doctor", "receptionist"])
        if st.button("Register"):
            register_user(username, password, role)
            st.success("Registration successful!")

    elif choice == "Add Doctor":
        if st.session_state.logged_in:
            # set_bg_from_local("mmmm.jpg")
            st.subheader("🩺 Add a new Doctor")
            name = st.text_input("Doctor Name")
            specialty = st.text_input("Specialty (e.g., Cardiologist, Neurologist)")
            if st.button("Add Doctor"):
                add_doctor(name, specialty)
                st.success(f"Doctor {name} ({specialty}) added!")
        else:
            st.warning("Please log in first.")

    elif choice == "Add Patient":
        if st.session_state.logged_in:
            # set_bg_from_local("as.jpg")
            st.subheader("👨‍⚕️ Add a new Patient")
            name = st.text_input("Patient Name")
            age = st.number_input("Age", min_value=0)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            address = st.text_area("Address")

            doctors = get_doctors()
            if doctors:
                doctor_choice = st.selectbox("Assign Doctor", [f"{doc[1]} ({doc[2]})" for doc in doctors])
                doctor_id = doctors[[f"{doc[1]} ({doc[2]})" for doc in doctors].index(doctor_choice)][0]
            else:
                st.warning("No doctors available!")
                doctor_id = None

            if st.button("Add Patient"):
                add_patient(name, age, gender, address, doctor_id)
                st.success("Patient added successfully!")
        else:
            st.warning("Please log in first.")

    elif choice == "View Patients":
        if st.session_state.logged_in:
            # set_bg_from_local("m.jpg")
            st.subheader("📋 Patient List")
            df = view_patients()
            if not df.empty:
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No patients found.")
        else:
            st.warning("Please log in first.")

    elif choice == "Logout":
        # st.session_state.logged_in = False
        # # set_bg_from_local("sa.jpg")
        # st.session_state.role = None
        # st.session_state.user_id = None
        st.success("🚪 You have been logged out.")
        # st.rerun()
         
if __name__ == "__main__":
    main()
