import pymongo

# init MongoDB API
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["github_database"]
language_collection = database["languages"]


# define method for removing users and their repos from database
def remove_user(username):
    user_collection = database[username]
    language_collection = database["language_collection"]
    for entry in user_collection.find():
        language_name = entry.get("name")
        total_repos = entry.get("total_repos")
        total_commits = entry.get("total_commits")
        total_branches = entry.get("total_branches")
        total_contributors = entry.get("total_contributors")
        total_size = entry.get("total_size")

        old_entry = language_collection.find_one({"name": language_name})

        new_total_repos = old_entry.get(
            "total_repos") - total_repos
        new_total_commits = old_entry.get(
            "total_commits") - total_commits
        new_total_branches = old_entry.get(
            "total_branches") - total_branches
        new_total_contributors = old_entry.get(
            "total_contributors") - total_contributors
        new_total_size = old_entry.get(
            "total_size") - total_size

        language_collection.delete_one({"name": language_name})

        if(new_total_repos > 0):
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

            language_collection.insert_one(new_entry)

    user_collection.drop()
