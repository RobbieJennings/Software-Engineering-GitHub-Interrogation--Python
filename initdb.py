import pymongo

# init MongoDB API
client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database("github_database")
database = client["github_database"]
language_collection = database["languages"]
