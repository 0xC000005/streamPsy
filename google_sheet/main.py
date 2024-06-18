# streamlit_app.py
# database location: https://docs.google.com/spreadsheets/d/1NwOWe6aZkAjGFjkC39ibOXTseaoQvEY4aeNhGwpcdRQ/edit?usp=sharing\

import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.add_vertical_space import add_vertical_space
import time
import numpy as np

st.set_page_config(
    page_title="StreamPsy Human Experiments Demo",
    page_icon="😎",
    menu_items={
        "Get Help": "https://www.extremelycoolapp.com/help",
        "Report a bug": "https://www.extremelycoolapp.com/bug",
        "About": "# This is a header. This is an *extremely* cool app!",
    },
)


# return a connection object
@st.cache_resource
def init_connection():
    # Create a connection object.
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn


conn = init_connection()

# initial the session UserData `PageID`
if "PageID" not in st.session_state:
    st.session_state.page_id = 1


def get_UserIDToPageID(conn: GSheetsConnection = conn):
    return conn.read(
        worksheet="UserIDToPageID",
        ttl=0,
        usecols=[0, 1, 2, 3],
        nrows=3,
    )


def get_users_pageID(user_id: int, conn: GSheetsConnection = conn):
    UserIDToPageID = get_UserIDToPageID(conn=conn)

    # get the PageID of the UserID
    page_id = UserIDToPageID.loc[0, "u" + str(user_id)]

    return page_id


def update_users_pageID(page_id: int, user_id: int, conn: GSheetsConnection = conn):
    UserIDToPageID = get_UserIDToPageID(conn=conn)

    # modify the first row of the column 'UserID' to the new PageID
    UserIDToPageID.loc[0, "u" + str(user_id)] = page_id

    # update the worksheet
    conn.update(
        worksheet="UserIDToPageID",
        data=UserIDToPageID,
    )

    # set the session state to the new PageID
    st.session_state.page_id = page_id


if st.session_state.page_id == 1:
    st.title("Welcome to the game")

    # display the markdown instructions
    st.markdown(
        """
        You can write your instructions in markdown. The app will render it for you.
        
        You can even put media here: 
        """
    )

    # display a youtube video
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    st.markdown(
        """
    ------
    """
    )

    # choose the player number using a click-on then submit button
    user_id = st.selectbox("What is your user ID?", ("1", "2", "3", "4"))

    st.write("You selected:", user_id)

    # move to the next PageID

    if st.button("Submit & Next"):
        st.session_state.UserID = user_id
        previous_page_id = get_users_pageID(user_id=user_id, conn=conn)
        if np.isnan(previous_page_id):
            update_users_pageID(page_id=2, user_id=user_id, conn=conn)
        else:
            # turn PageID from np.float64 to int
            update_users_pageID(
                page_id=int(previous_page_id), user_id=user_id, conn=conn
            )
        st.rerun()


if st.session_state.page_id == 2:
    st.title("You are now at PageID 2")
    st.write("You have selected player number: ", st.session_state.UserID)

    if st.button("Go to PageID 3"):
        update_users_pageID(page_id=3, user_id=st.session_state.UserID, conn=conn)
        st.rerun()


if st.session_state.page_id == 3:

    st.title("You are now at PageID 3")
    st.write("You have selected player number: ", st.session_state.UserID)
    st.write("You have to wait at this page until all players are in page 3")

    with st.spinner("Wait for it other users to reach page 3..."):
        placeholder = st.empty()
        while True:

            num_user_reached = 0
            UserIDToPageID = get_UserIDToPageID(conn=conn)
            # check if all u1, u2, u3, u4 are in page 3
            for i in range(1, 5):
                if UserIDToPageID.loc[0, "u" + str(i)] >= 3:
                    num_user_reached += 1
            if num_user_reached >= 4:
                break
            else:
                placeholder.empty()
                placeholder.write(f"{num_user_reached}/4 users have reached page 3")

            time.sleep(10)

    update_users_pageID(page_id=4, user_id=st.session_state.UserID, conn=conn)
    st.rerun()


if st.session_state.page_id == 4:
    st.title("You are now at PageID 4")
    st.write("You have selected player number: ", st.session_state.UserID)

    # post a example question

    st.write("Question 1: Choose the following image that represent Will")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")
        if st.button("Select", key="cat"):
            # write a session state: selected
            st.session_state.selected = "cat"


    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")
        if st.button("Select", key="dog"):
            # write a session state: selected
            st.session_state.selected = "dog"


    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")
        st.button("Select", key="owl")

        if st.button("Select", key="owl"):
            # write a session state: selected
            st.session_state.selected = "owl"


    # display the selected image
    if "selected" in st.session_state:
        st.write("You selected the image of a", st.session_state.selected)
    pass


