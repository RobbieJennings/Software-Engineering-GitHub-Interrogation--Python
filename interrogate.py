from github import Github
import pymongo

# init github API
g = Github("4986e75bbfff142ff1550dcbca813ba0d6d872e3")

# init MongoDB API
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["github_database"]

# init language collection
language_collection = database["languages"]
language_entry = {"name": "Java", "total_repos": 1,
                  "avg_commits": 1, "avg_branches": 1, "avg_contributors": 1,
                  "avg_size": 1}
x = language_collection.insert_one(language_entry)

# check database
print(client.list_database_names())
print(database.list_collection_names())

users = []

source = "RobbieJennings"

sourceUser = g.get_user(source)

if(sourceUser not in users):
    users.append(sourceUser)

for follower in sourceUser.get_following():
    if(follower not in users):
        users.append(follower)

for following in sourceUser.get_followers():
    if(following not in users):
        users.append(following)

# for user in users:
#     username = user.login
#     for repo in user.get_repos():
#         if(repo.size > 0):
#             numCommits = repo.get_commits().totalCount
#             numBranches = repo.get_branches().totalCount
#             numContributors = repo.get_contributors().totalCount
#             size = repo.size
#             for language in repo.get_languages():
#                 print(username)
#                 print(language)
#                 print(size)
#                 print(numCommits)
#                 print(numBranches)
#                 print(numContributors)
#                 print()
#         print("----------")
#     print("++++++++++")
#     # Put this data in database
