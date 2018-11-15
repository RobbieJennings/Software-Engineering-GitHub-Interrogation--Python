from github import Github
import pymongo

# init github API
g = Github("4986e75bbfff142ff1550dcbca813ba0d6d872e3")

# init MongoDB API
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["github_database"]

# init language collection
language_collection = database["languages"]

# init userbase
source = "RobbieJennings"
sourceUser = g.get_user(source)
users = []

if(sourceUser not in users):
    users.append(sourceUser)

for follower in sourceUser.get_following():
    if(follower not in users):
        users.append(follower)

for following in sourceUser.get_followers():
    if(following not in users):
        users.append(following)

# populate database
for user in users:
    username = user.login
    for repo in user.get_repos():
        if(repo.size > 0):
            total_commits = repo.get_commits().totalCount
            total_branches = repo.get_branches().totalCount
            total_contributors = repo.get_contributors().totalCount
            total_size = repo.size

            for language in repo.get_languages():
                old_entry = language_collection.find_one(language)

                if(old_entry is not None):
                    new_total_repos = old_entry.find(
                        "total_repos") + 1
                    new_total_commits = old_entry.find(
                        "total_commits") + total_commits
                    new_total_branches = old_entry.find(
                        "total_branches") + total_branches
                    new_total_contributors = old_entry.find(
                        "total_contributors") + total_contributors
                    new_total_size = old_entry.find(
                        "total_size") + total_size
                    language_collection.delete_one(language)
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

print("done")
