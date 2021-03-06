import pymongo
import json
import sys

# init MongoDB API
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client["github_database"]
language_collection = database["language_collection"]


# define method for returning relevant statistics as JSON
def get_statistics(username):
    stats = []
    max = [0, 0, 0, 0]
    user_collection = None

    if(username is not None and username in database.collection_names()):
        user_collection = database[username]
        cursor = user_collection.find({})
        for document in cursor:
            name = document.get("name")
            avg_commits = document.get("avg_commits")
            avg_branches = document.get("avg_branches")
            avg_contributors = document.get("avg_contributors")
            avg_size = document.get("avg_size")

            generic_stats = language_collection.find_one({"name": name})
            generic_commits = generic_stats.get("avg_commits")
            generic_branches = generic_stats.get("avg_branches")
            generic_contributors = generic_stats.get("avg_contributors")
            generic_size = generic_stats.get("avg_size")

            if(avg_commits > max[0]):
                max[0] = avg_commits
            if(avg_branches > max[1]):
                max[1] = avg_branches
            if(avg_contributors > max[2]):
                max[2] = avg_contributors
            if(avg_size > max[3]):
                max[3] = avg_size
            if(generic_commits > max[0]):
                max[0] = generic_commits
            if(generic_branches > max[1]):
                max[1] = generic_branches
            if(generic_contributors > max[2]):
                max[2] = generic_contributors
            if(generic_size > max[3]):
                max[3] = generic_size

            new_entry = {"name": name,
                         "avg_commits": avg_commits,
                         "generic_commits": generic_commits,
                         "avg_branches": avg_branches,
                         "generic_branches": generic_branches,
                         "avg_contributors": avg_contributors,
                         "generic_contributors": generic_contributors,
                         "avg_size": avg_size,
                         "generic_size": generic_size}
            stats.append(new_entry)

    cursor = language_collection.find({})
    for document in cursor:
        name = document.get("name")
        if(user_collection is None
           or user_collection.find({"name": name}).count() == 0):
            avg_commits = 0
            avg_branches = 0
            avg_contributors = 0
            avg_size = document = 0

            generic_stats = language_collection.find_one({"name": name})
            generic_commits = generic_stats.get("avg_commits")
            generic_branches = generic_stats.get("avg_branches")
            generic_contributors = generic_stats.get("avg_contributors")
            generic_size = generic_stats.get("avg_size")

            if(generic_commits > max[0]):
                max[0] = generic_commits
            if(generic_branches > max[1]):
                max[1] = generic_branches
            if(generic_contributors > max[2]):
                max[2] = generic_contributors
            if(generic_size > max[3]):
                max[3] = generic_size

            new_entry = {"name": name,
                         "avg_commits": avg_commits,
                         "generic_commits": generic_commits,
                         "avg_branches": avg_branches,
                         "generic_branches": generic_branches,
                         "avg_contributors": avg_contributors,
                         "generic_contributors": generic_contributors,
                         "avg_size": avg_size,
                         "generic_size": generic_size}
            stats.append(new_entry)

    data = {"max": max, "stats": stats}
    return json.dumps(data)


if __name__ == "__main__":
    if(len(sys.argv) > 1):
        sys.stdout.write(get_statistics(sys.argv[1]))
    else:
        sys.stdout.write(get_statistics(None))
    sys.stdout.flush()
