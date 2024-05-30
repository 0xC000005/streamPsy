import streamlit as st
import sqlite3


# Function to fetch data from the database
def fetch_data():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    data = c.fetchall()
    conn.close()
    return data


# Function to write data to the database
def write_data(row_num: int, left: int = None, right: int = None):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    if left is not None:
        c.execute(f"UPDATE data SET LEFT = {left} WHERE rowid = {row_num}")
    elif right is not None:
        c.execute(f"UPDATE data SET RIGHT = {right} WHERE rowid = {row_num}")
    else:
        raise ValueError("You must provide a value for either left or right")
    conn.commit()
    conn.close()
    # Clear the cache after writing data to force refetching the updated data
    cached_fetch_data.clear()


# Cache the data fetching function
@st.cache_data
def cached_fetch_data():
    return fetch_data()


# Initialize a Streamlit app that will display the LEFT and RIGHT at row 1 in real time and update these numbers by
# the user input.
st.title("Streamlit App")
st.write(
    "This app will display the LEFT and RIGHT columns of the first row in real time and update these numbers by the user input."
)

data = cached_fetch_data()
left = data[0][0]
right = data[0][1]
st.write(f"LEFT: {left}")
st.write(f"RIGHT: {right}")

# Get the user input of the left number with a submit button
left_input = st.number_input("Enter the LEFT number", value=left)
if st.button("Submit"):
    write_data(1, left=left_input)
    st.rerun()

# display the Duolingo like image selection task
with st.container():
    st.write("Select the image that best describes the word")
    # word: cat, in large size. make it centered
    with st.columns(3)[1]:
        st.header("Cat")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.image("img/1.jpg", use_column_width=True)
        if st.button("Select", key="1"):
            st.session_state["button"] = 1

    with col2:
        st.image("img/2.jpg", use_column_width=True)
        if st.button("Select", key="2"):
            st.session_state["button"] = 2

    with col3:
        st.image("img/3.jpg", use_column_width=True)
        if st.button("Select", key="3"):
            st.session_state["button"] = 3

    with col4:
        st.image("img/4.jpg", use_column_width=True)
        if st.button("Select", key="4"):
            st.session_state["button"] = 4

    # display the selected image
    if "button" in st.session_state:
        st.write(f"Selected image: {st.session_state['button']}")
    else:
        st.write("No image selected")

if __name__ == "__main__":
    pass
