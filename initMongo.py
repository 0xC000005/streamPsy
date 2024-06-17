# initialized the mongoDB

# first connect to the mongoDB
import pymongo

# connect to the mongoDB
def connect_to_mongoDB():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["SocialAI"]
    return db

# create a collection
def create_collection(db):
    collection = db["UserIDToPageID"]
    return collection


if __name__ == '__main__':
    db = connect_to_mongoDB()
    collection = create_collection(db)
    print("collection created")
    print("db connected")
    # insert a document
    collection.insert_one({"UserID": 1, "PageID": 1})
    print("document inserted")

    # find the document with UserID = 1
    user_id = 1
    document = collection.find_one({"UserID": user_id})

    # printout the pageid of the UserID
    print(f"PageID of UserID {user_id} is {document['PageID']}")


    # close the connection
    db.client.close()
