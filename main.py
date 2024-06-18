# streamlit_app.py
from typing import Any, Mapping
import streamlit as st
import time
import json
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


def get_counts_from_ProblemID(
        ProblemID: int, conn: Database[Mapping[str, Any] | Any] = CONN
):
    collection = conn["Problem"]
    document = collection.find_one({"ProblemID": ProblemID})
    if document is None:
        return None
    else:
        # return the `count` field
        return document["ProblemID"]


def increase_count_of_problemID(
        ProblemID: int, conn: Database[Mapping[str, Any] | Any] = CONN
):
    collection = conn["Problem"]
    document = collection.find_one({"ProblemID": ProblemID})
    if document is None:
        collection.insert_one({"ProblemID": ProblemID, "count": 1})
    else:
        # increase the `count` field by 1
        collection.update_one({"ProblemID": ProblemID}, {"$inc": {"count": 1}})


def get_total_num_of_user(conn: Database[Mapping[str, Any] | Any] = CONN):
    collection = conn["UserIDToPageID"]
    return collection.count_documents({})


def get_user_specific_data(UserID: int, conn: Database[Mapping[str, Any] | Any] = CONN):
    # this function is for storing not frequently accessed user-specific data,
    # the reason why users PageID is not stored here is that the PageID is frequently read and written
    # and the eval function is not efficient for frequently accessed data
    collection = conn["UserData"]
    document = collection.find_one({"UserID": UserID})
    # get the UserData field
    UserData = document["UserData"]
    # turn the UserData from string to dictionary
    return json.loads(UserData)


def update_user_specific_data(UserID: int, UserData: dict, conn: Database[Mapping[str, Any] | Any] = CONN):
    collection = conn["UserData"]
    # if the document does not exist, insert a new document, else update the document
    collection.update_one({"UserID": UserID}, {"$set": {"UserData": json.dumps(UserData)}}, upsert=True)


def wait_until_all_users_reached_page(PageID_to_reach: int):
    total_num_of_user = get_total_num_of_user()
    with st.spinner(
            "Wait for it other users to reach page " + str(PageID_to_reach) + "..."
    ):
        placeholder = st.empty()

        while True:
            num_of_user_have_reached_page_x = 0
            # check if userID 1, 2, 3, 4 are at least in page 3
            for i in range(1, total_num_of_user + 1):
                if get_UserIDToPageID(i, conn=CONN) >= PageID_to_reach:
                    num_of_user_have_reached_page_x += 1
            if num_of_user_have_reached_page_x >= 4:
                break
            else:
                placeholder.empty()
                placeholder.write(
                    f"{num_of_user_have_reached_page_x}/{total_num_of_user} users have reached page "
                    + str(PageID_to_reach)
                    + "..."
                )

            time.sleep(3)


# ============== Streamlit App ==============


# initial the session UserData `PageID`
if "PageID" not in st.session_state:
    st.session_state.PageID = 1

# ============= Page 1 =============

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

    # choose the player number using a click-on then submitting button
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

# ============= Page 2 =============

if st.session_state.PageID == 2:
    st.title("You are now at PageID 2")
    st.write("You have selected player number: ", st.session_state.UserID)

    if st.button("Go to PageID 3"):
        update_users_pageID(PageID=3, UserID=st.session_state.UserID, conn=CONN)
        st.rerun()

# ============= Page 3 =============

if st.session_state.PageID == 3:
    st.title("You are now at PageID 3")
    st.write("You have selected player number: ", st.session_state.UserID)
    st.write("You have to wait at this page until all players are in page 3")

    wait_until_all_users_reached_page(PageID_to_reach=3)

    update_users_pageID(PageID=4, UserID=st.session_state.UserID, conn=CONN)

    st.rerun()

# ============= Page 4 =============

if st.session_state.PageID == 4:

    st.title("You are now at PageID 4")
    st.write("You have selected player number: ", st.session_state.UserID)

    # post an example question

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

    if st.button("Submit & Next"):
        update_users_pageID(PageID=5, UserID=st.session_state.UserID, conn=CONN)

        # create a mapping from st.session_state.selected to ProblemID
        mapping = {"cat": 1, "dog": 2, "owl": 3}
        ProblemID = mapping[st.session_state.selected]

        increase_count_of_problemID(ProblemID=ProblemID, conn=CONN)
        st.rerun()

# ============= Page 5 =============

if st.session_state.PageID == 5:
    st.title("You are now at PageID 5")
    st.write("You have selected player number: ", st.session_state.UserID)

    # post an example question

    st.write("Question 1: Choose the following image that represent Will")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("A cat")
        st.image("https://static.streamlit.io/examples/cat.jpg")
        # show the count of the ProblemID
        count = get_counts_from_ProblemID(ProblemID=1, conn=CONN)
        st.write(f"Count: {count}")
        if st.button("Select", key="cat"):
            # write a session state: selected
            st.session_state.selected = "cat"

    with col2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg")
        # show the count of the ProblemID
        count = get_counts_from_ProblemID(ProblemID=2, conn=CONN)
        st.write(f"Count: {count}")
        if st.button("Select", key="dog"):
            # write a session state: selected
            st.session_state.selected = "dog"

    with col3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg")
        count = get_counts_from_ProblemID(ProblemID=3, conn=CONN)
        st.write(f"Count: {count}")
        if st.button("Select", key="owl"):
            # write a session state: selected
            st.session_state.selected = "owl"

    # display the selected image
    if "selected" in st.session_state:
        st.write("You selected the image of a", st.session_state.selected)

    # for a page that has a button as well as waiting mechanism, we need to make sure the button press state is
    # remembered even if the user refreshes the page

    if st.button("Submit & Next"):
        # Set a cookie

        update_users_pageID(PageID=6, UserID=st.session_state.UserID, conn=CONN)
        wait_until_all_users_reached_page(PageID_to_reach=5)
        st.rerun()

# ============= Page 6 =============

if st.session_state.PageID == 6:
    st.title("You are now at PageID 6")
    st.write("You have selected player number: ", st.session_state.UserID)
    st.write("You have completed the experiment. Thank you for your participation!")
