from pprint import pprint
import pymongo
import initdb
import removeuser
import adduser

# init database
initdb.init()

# insert users
adduser.insert_user("RobbieJennings")
adduser.insert_user("luandry")

# remove user
removeuser.remove_user("RobbieJennings")

# check database
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["github_database"]

for collection in database.list_collection_names():
    if(collection != "language_collection"):
        print(collection)
        cursor = database[collection].find({})
        for document in cursor:
            pprint(document)

print("language_collection")
cursor = database["language_collection"].find({})
for document in cursor:
    pprint(document)
