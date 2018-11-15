import pymongo


# init MongoDB API
def init():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    client.drop_database("github_database")
    database = client["github_database"]
    database["languages"]
