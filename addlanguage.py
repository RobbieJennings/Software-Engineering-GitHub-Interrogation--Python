from github import Github
import pymongo

# init github API
g = Github("4986e75bbfff142ff1550dcbca813ba0d6d872e3")

# init MongoDB API
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["github_database"]
language_collection = database["languages"]


# define method for inserting languages into database
def insert_language(collection_name, language_name, total_commits,
                    total_branches, total_contributors, total_size):
    collection = database[collection_name]
    old_entry = collection.find_one({"name": language_name})

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
        collection.delete_one({"name": language_name})
    else:
        new_total_repos = 1
        new_total_commits = total_commits
        new_total_branches = total_branches
        new_total_contributors = total_contributors
        new_total_size = total_size

    new_name = language_name
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

    collection.insert_one(new_entry)
