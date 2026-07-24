import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/employees/"

st.set_page_config(page_title="Employee Manager", layout="wide")
st.title("Employee Management System")
tab1, tab2 = st.tabs([" View & Manage", " Add Employee"])
# --- TAB 1: VIEW, UPDATE, DELETE ---
with tab1:
    res = requests.get(API_URL)
    if res.status_code == 200:
        employees = res.json()
        for emp in employees:
            with st.expander(f"{emp['name']} - {emp['department']}"):
                # Update Form within Expander
                new_name = st.text_input("Name", emp['name'], key=f"n{emp['id']}")
                new_dept = st.text_input("Dept", emp['department'], key=f"d{emp['id']}")
                new_sal = st.number_input("Salary", value=float(emp['salary']), key=f"s{emp['id']}")
                
                col1, col2 = st.columns(2)
                if col1.button("Update Info", key=f"up{emp['id']}"):
                    payload = {"name": new_name, "department": new_dept, "salary": new_sal}
                    requests.put(f"{API_URL}{emp['id']}", json=payload)
                    st.rerun()
                
                if col2.button(" Delete Employee", key=f"del{emp['id']}"):
                    requests.delete(f"{API_URL}{emp['id']}")
                    st.rerun()

# --- TAB 2: CREATE ---
with tab2:
    with st.form("add_form"):
        name = st.text_input("Employee Name")
        dept = st.selectbox("Department", ["HR", "IT", "Sales", "Finance"])
        salary = st.number_input("Annual Salary", min_value=0.0)
        if st.form_submit_button("Add to Database"):
            requests.post(API_URL, json={"name": name, "department": dept, "salary": salary})
            st.success(f"Added {name}!")