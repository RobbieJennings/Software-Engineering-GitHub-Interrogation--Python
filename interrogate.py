from github import Github

g = Github("4986e75bbfff142ff1550dcbca813ba0d6d872e3")

for repo in g.get_user().get_repos():
    print(repo.name)
