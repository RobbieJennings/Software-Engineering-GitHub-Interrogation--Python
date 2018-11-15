from github import Github
import pymongo
import addlanguage
import removeuser

# init github API
g = Github("4986e75bbfff142ff1550dcbca813ba0d6d872e3")

# init MongoDB API
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["github_database"]
language_collection = database["languages"]


# define method for inserting users and their repos into database
def insert_user(username):
    user = g.get_user(username)
    if(username in database.list_collection_names()):
        removeuser.remove_user(username)
    else:
        database[username]
    for repo in user.get_repos():
        if(repo.size > 0):
            total_commits = repo.get_commits().totalCount
            total_branches = repo.get_branches().totalCount
            total_contributors = repo.get_contributors().totalCount
            total_size = repo.size

            for language in repo.get_languages():
                addlanguage.insert_language(username, language, total_commits,
                                            total_branches, total_contributors,
                                            total_size)
                addlanguage.insert_language("language_collection", language,
                                            total_commits, total_branches,
                                            total_contributors, total_size)
