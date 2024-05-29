import streamlit as st
import pandas as pd
from filelock import FileLock, Timeout
import time

# File path for the CSV file
csv_file = "numbers.csv"
lock_file = "numbers.csv.lock"


# Function to read the numbers from the CSV file
def read_numbers():
    with FileLock(lock_file):
        df = pd.read_csv(csv_file)
        return df.loc[0, "left_number"], df.loc[0, "right_number"]


# Function to update the numbers in the CSV file
def update_numbers(left, right):
    with FileLock(lock_file):
        df = pd.DataFrame({"left_number": [left], "right_number": [right]})
        df.to_csv(csv_file, index=False)


# Read the initial numbers
left_number, right_number = read_numbers()

# Initialize session state
if "left_number" not in st.session_state:
    st.session_state.left_number = left_number
if "right_number" not in st.session_state:
    st.session_state.right_number = right_number

# Get the role of the user (left or right)
role = st.sidebar.selectbox("Select Role", options=["left", "right"])


# Function to update the left number
def update_left_number(new_value):
    try:
        with FileLock(lock_file, timeout=5):
            st.session_state.left_number = new_value
            update_numbers(st.session_state.left_number, st.session_state.right_number)
    except Timeout:
        st.error(
            "File is currently being edited by another user. Please wait and try again."
        )


# Function to update the right number
def update_right_number(new_value):
    try:
        with FileLock(lock_file, timeout=5):
            st.session_state.right_number = new_value
            update_numbers(st.session_state.left_number, st.session_state.right_number)
    except Timeout:
        st.error(
            "File is currently being edited by another user. Please wait and try again."
        )


# Display both numbers
st.header("Current Numbers")
st.write(f"Left Number: {st.session_state.left_number}")
st.write(f"Right Number: {st.session_state.right_number}")

if role == "left":
    st.header("User A (Left)")
    left_input = st.number_input(
        "Enter a new number for User A",
        value=st.session_state.left_number,
        key="left_input",
    )
    if st.button("Update Left Number"):
        update_left_number(left_input)
        st.experimental_rerun()
else:
    st.header("User B (Right)")
    right_input = st.number_input(
        "Enter a new number for User B",
        value=st.session_state.right_number,
        key="right_input",
    )
    if st.button("Update Right Number"):
        update_right_number(right_input)
        st.experimental_rerun()

# Synchronize the numbers with the CSV file
try:
    with FileLock(lock_file, timeout=5):
        left_number, right_number = read_numbers()
        if (
            left_number != st.session_state.left_number
            or right_number != st.session_state.right_number
        ):
            st.session_state.left_number = left_number
            st.session_state.right_number = right_number
            st.experimental_rerun()
except Timeout:
    st.write("Waiting for the file to be available...")
    time.sleep(2)
    st.experimental_rerun()
