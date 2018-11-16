import pymongo
import sys


# init MongoDB API
def init():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    client.drop_database("github_database")
    database = client["github_database"]
    database["languages"]
    return "successfully initialised database"


if __name__ == "__main__":
    print(init())
    sys.stdout.flush()
