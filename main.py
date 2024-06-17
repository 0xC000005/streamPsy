# streamlit_app.py
from typing import Any, Mapping
import streamlit as st
import time
import pymongo
from pymongo.database import Database

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
def init_connection() -> Database[Mapping[str, Any] | Any]:
    # connect to the MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["SocialAI"]
    return db


CONN = init_connection()


def get_UserIDToPageID(UserID: int, conn: Database[Mapping[str, Any] | Any] = CONN):

    # read the UserIDtoPageID collection from the mongoDB
    collection = conn["UserIDToPageID"]

    # find the document with UserID, if the document does not exist, return None
    document = collection.find_one({"UserID": UserID})

    # return the PageID of the UserID
    if document is not None:
        return document["PageID"]
    else:
        return None


def update_users_pageID(
    PageID: int, UserID: int, conn: Database[Mapping[str, Any] | Any] = CONN
):
    # update the PageID of the UserID
    collection = conn["UserIDToPageID"]

    # find the document with UserID
    document = collection.find_one({"UserID": UserID})

    if document is None:
        # if the document does not exist, insert a new document
        collection.insert_one({"UserID": UserID, "PageID": PageID})
    else:
        # if the document exists, update the PageID
        collection.update_one({"UserID": UserID}, {"$set": {"PageID": PageID}})

    # set the session state to the new PageID
    st.session_state.PageID = PageID


# ============== Streamlit App ==============


# initial the session data `PageID`
if "PageID" not in st.session_state:
    st.session_state.PageID = 1

if st.session_state.PageID == 1:
    st.title("Welcome to the StreamPsy Human Experiments Demo")

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
    UserID = st.selectbox("What is your UserID?", ("1", "2", "3", "4"))
    UserID = int(UserID)

    st.write("You selected:", UserID)

    # move to the next PageID

    if st.button("Submit & Next"):
        st.session_state.UserID = UserID
        PageID = get_UserIDToPageID(UserID=UserID, conn=CONN)
        if PageID is None:
            # the User hasn't logged in before, go to page 2
            update_users_pageID(PageID=2, UserID=UserID, conn=CONN)
            st.write(st.session_state.PageID)
        else:
            # the User has logged in before, go to the page where the User left
            st.session_state.PageID = PageID
            st.write(st.session_state.PageID)
        st.rerun()

if st.session_state.PageID == 2:
    st.title("You are now at PageID 2")
    st.write("You have selected player number: ", st.session_state.UserID)

    if st.button("Go to PageID 3"):
        update_users_pageID(PageID=3, UserID=st.session_state.UserID, conn=CONN)
        st.rerun()

if st.session_state.PageID == 3:

    st.title("You are now at PageID 3")
    st.write("You have selected player number: ", st.session_state.UserID)
    st.write("You have to wait at this page until all players are in page 3")

    with st.spinner("Wait for it other users to reach page 3..."):
        placeholder = st.empty()
        while True:

            num_of_user_have_reached_page_3 = 0
            # check if userID 1, 2, 3, 4 are at least in page 3
            for i in range(1, 5):
                if get_UserIDToPageID(i, conn=CONN) >= 3:
                    num_of_user_have_reached_page_3 += 1
            if num_of_user_have_reached_page_3 >= 4:
                break
            else:
                placeholder.empty()
                placeholder.write(f"{num_of_user_have_reached_page_3}/4 users have reached page 3")

            time.sleep(3)

    update_users_pageID(PageID=4, UserID=st.session_state.UserID, conn=CONN)

    st.rerun()

if st.session_state.PageID == 4:
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

        if st.button("Select", key="owl"):
            # write a session state: selected
            st.session_state.selected = "owl"

    # display the selected image
    if "selected" in st.session_state:
        st.write("You selected the image of a", st.session_state.selected)
    pass
