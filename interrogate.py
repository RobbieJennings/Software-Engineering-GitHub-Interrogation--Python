from github import Github

g = Github("4986e75bbfff142ff1550dcbca813ba0d6d872e3")
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

for user in users:
    username = user.login
    for repo in user.get_repos():
        numCommits = repo.get_commits().totalCount
        numBranches = repo.get_branches().totalCount
        numContributors = repo.get_contributors().totalCount
        size = repo.size
        for language in repo.get_languages():
            print(username)
            print(language)
            print(size)
            print(numCommits)
            print(numBranches)
            print(numContributors)
            print()
        print("----------")
    print("++++++++++")
    # Put this data in database
