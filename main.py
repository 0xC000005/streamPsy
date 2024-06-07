# streamlit_app.py
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_extras.add_vertical_space import add_vertical_space
import time
import numpy as np

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
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

# initial the session data `page_id`
if "page_id" not in st.session_state:
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

    # get the page_id of the user_id
    page_id = UserIDToPageID.loc[0, "u" + str(user_id)]

    return page_id


def update_users_pageID(page_id: int, user_id: int, conn: GSheetsConnection = conn):
    UserIDToPageID = get_UserIDToPageID(conn=conn)

    # modify the first row of the column 'user_id' to the new page_id
    UserIDToPageID.loc[0, "u" + str(user_id)] = page_id

    # update the worksheet
    conn.update(
        worksheet="UserIDToPageID",
        data=UserIDToPageID,
    )

    # set the session state to the new page_id
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

    # move to the next page_id

    if st.button("Submit & Next"):
        st.session_state.user_id = user_id
        previous_page_id = get_users_pageID(user_id=user_id, conn=conn)
        if np.isnan(previous_page_id):
            update_users_pageID(page_id=2, user_id=user_id, conn=conn)
        else:
            # turn previous_page_id from np.float64 to int
            update_users_pageID(
                page_id=int(previous_page_id), user_id=user_id, conn=conn
            )
        st.rerun()

if st.session_state.page_id == 2:
    st.title("You are now at page_id 2")
    st.write("You have selected player number: ", st.session_state.user_id)

    if st.button("Go to page_id 3"):
        update_users_pageID(page_id=3, user_id=st.session_state.user_id, conn=conn)
        st.rerun()

if st.session_state.page_id == 3:

    st.title("You are now at page_id 3")
    st.write("You have selected player number: ", st.session_state.user_id)
    st.write("You have to wait at this page until all players are in page 3")

    with st.spinner("Wait for it other users to reach page 3..."):
        placeholder = st.empty()
        while True:

            num_user_reached = 0
            UserIDToPageID = get_UserIDToPageID(conn=conn)
            # check if all u1, u2, u3, u4 are in page 3
            for i in range(1, 5):
                if UserIDToPageID.loc[0, "u" + str(i)] == 3:
                    num_user_reached += 1
            if num_user_reached == 4:
                break
            else:
                placeholder.empty()
                placeholder.write(f"{num_user_reached}/4 users have reached page 3")
            time.sleep(10)

    update_users_pageID(page_id=4, user_id=st.session_state.user_id, conn=conn)
    st.rerun()

if st.session_state.page_id == 4:
    st.title("You are now at page_id 4")
    st.write("You have selected player number: ", st.session_state.user_id)
    pass
