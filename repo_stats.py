
import os
from github import Github
from location_resolver import Location_Resolver


def repo_stats(repo_path):
    gh = Github(os.getenv("GITHUB_MAP_USERNAME", ""), \
                os.getenv("GITHUB_MAP_PASSWORD", ""))
    lr = Location_Resolver(gh)

    repo = gh.get_repo(repo_path)
    stats = repo.get_stats_contributors()

    unknown_users = 0
    unknown_commits = 0
    commits_by_location = {}

    # stats will be a list of StatsContributor objects
    for contributor in stats:

        # there are cases where a contributor can't be found anymore
        if contributor.author:
            username = contributor.author.login
            location_str = contributor.author.location
            # print(username, location_str)
            # in this case, we already have the location string
            location = lr(contributor.author.login, contributor.author.location)
            commits_by_location[location] = commits_by_location.get(location, 0) + contributor.total
        else:
            unknown_users += 1
            unknown_commits += contributor.total

    # debug
    for location, commits in commits_by_location.items():
        print(str(location), commits)


if __name__ == "__main__":
    repo_stats("brendan-w/python-OBD")
