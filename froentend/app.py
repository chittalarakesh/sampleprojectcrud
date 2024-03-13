import streamlit as st
import requests



st.title("Submit Form Details")

name = st.text_input("Name")
email = st.text_input("Email")

if st.button("Submit"):
    if name!="" and email!="":
        response = requests.post("http://backend:8000/submit_form/", json={"name": name, "email": email})
        if response.status_code == 200:
            st.success("Form submitted successfully")
        else:
            st.error("Failed to submit form")

st.title("Get Details")

if st.button("getdetails"):
     response = requests.get("http://backend:8000/get_details")
     if response.status_code==200:
          data = response.json()  # Assuming the response is in JSON format
          st.table(data)

BASE_URL="http://backend:8000/"
DELETE_ENDPOINT="delete_record"
          
st.title("Delete Record")
record_id = st.text_input("Enter ID of the record to delete:")
if st.button("Delete Record"):
    response = requests.delete(f"{BASE_URL}{DELETE_ENDPOINT}/{int(record_id)}")
    if response.status_code == 200:
        st.success(f"Record with ID {record_id} deleted successfully.")
    else:
        st.error("Failed to delete the record.")


st.title('Update Form Record')

# Form fields to be filled out by the user
form_id = st.number_input('Form ID', min_value=1, value=1, step=1)
name = st.text_input('UpdateName')
email = st.text_input('UpdateEmail')

UPDATE_BASE_URL="http://backend:8000/"

# Button to send the PUT request
if st.button('Update Form'):
    update_endpoint = f"{UPDATE_BASE_URL}update_form/{int(form_id)}"
    form_data = {"name": name, "email": email}
    
    # Sending a PUT request to the FastAPI backend
    response = requests.put(update_endpoint, json=form_data)
     
    if response.status_code == 200:
        st.success('Form updated successfully.')
    else:
        st.error('Failed to update form.')