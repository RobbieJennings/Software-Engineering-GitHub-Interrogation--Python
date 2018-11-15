from github import Github
from pprint import pprint
import pymongo

# init github API
g = Github("4986e75bbfff142ff1550dcbca813ba0d6d872e3")

# init MongoDB API
client = pymongo.MongoClient("mongodb://localhost:27017/")
client.drop_database("github_database")
database = client["github_database"]
language_collection = database["languages"]

# init user
username = "RobbieJennings"
user = g.get_user(username)

# populate database
if(username not in database.list_collection_names()):
    user_collection = database[username]
    for repo in user.get_repos():
        if(repo.size > 0):
            total_commits = repo.get_commits().totalCount
            total_branches = repo.get_branches().totalCount
            total_contributors = repo.get_contributors().totalCount
            total_size = repo.size

            for language in repo.get_languages():
                old_entry = user_collection.find_one({"name": language})
                if(old_entry is not None):
                    new_total_repos = old_entry.get(
                        "total_repos") + 1
                    new_total_commits = old_entry.get(
                        "total_commits") + total_commits
                    new_total_branches = old_entry.get(
                        "total_branches") + total_branches
                    new_total_contributors = old_entry.get(
                        "total_contributors") + total_contributors
                    new_total_size = old_entry.get(
                        "total_size") + total_size
                    language_collection.delete_one({"name": language})
                else:
                    new_total_repos = 1
                    new_total_commits = total_commits
                    new_total_branches = total_branches
                    new_total_contributors = total_contributors
                    new_total_size = total_size

                new_name = language
                new_avg_commits = new_total_commits / new_total_repos
                new_avg_branches = new_total_branches / new_total_repos
                new_avg_contributors = new_total_contributors / new_total_repos
                new_avg_size = new_total_size / new_total_repos

                new_entry = {"name": new_name,
                             "total_repos": new_total_repos,
                             "total_commits": new_total_commits,
                             "avg_commits": new_avg_commits,
                             "total_branches": new_total_branches,
                             "avg_branches": new_avg_branches,
                             "total_contributors": new_total_contributors,
                             "avg_contributors": new_avg_contributors,
                             "total_size": new_total_size,
                             "avg_size": new_avg_size}

                user_collection.insert_one(new_entry)

                old_entry = language_collection.find_one({"name": language})
                if(old_entry is not None):
                    new_total_repos = old_entry.get(
                        "total_repos") + 1
                    new_total_commits = old_entry.get(
                        "total_commits") + total_commits
                    new_total_branches = old_entry.get(
                        "total_branches") + total_branches
                    new_total_contributors = old_entry.get(
                        "total_contributors") + total_contributors
                    new_total_size = old_entry.get(
                        "total_size") + total_size
                    language_collection.delete_one({"name": language})
                else:
                    new_total_repos = 1
                    new_total_commits = total_commits
                    new_total_branches = total_branches
                    new_total_contributors = total_contributors
                    new_total_size = total_size

                new_name = language
                new_avg_commits = new_total_commits / new_total_repos
                new_avg_branches = new_total_branches / new_total_repos
                new_avg_contributors = new_total_contributors / new_total_repos
                new_avg_size = new_total_size / new_total_repos

                new_entry = {"name": new_name,
                             "total_repos": new_total_repos,
                             "total_commits": new_total_commits,
                             "avg_commits": new_avg_commits,
                             "total_branches": new_total_branches,
                             "avg_branches": new_avg_branches,
                             "total_contributors": new_total_contributors,
                             "avg_contributors": new_avg_contributors,
                             "total_size": new_total_size,
                             "avg_size": new_avg_size}

                language_collection.insert_one(new_entry)

for collection in database.list_collection_names():
    if(collection != "language_collection"):
        print(collection)
        cursor = database[collection].find({})
        for document in cursor:
            pprint(document)

print("language_collection")
cursor = language_collection.find({})
for document in cursor:
    pprint(document)
