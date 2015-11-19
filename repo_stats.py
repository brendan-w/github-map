
import os
from github import Github
from location_resolver import Location_Resolver


def repo_stats(repo_path):
    gh = Github(os.getenv("GITHUB_MAP_USERNAME", ""), \
                os.getenv("GITHUB_MAP_PASSWORD", ""))
    lr = Location_Resolver(gh)

    repo = gh.get_repo(repo_path)
    stats = repo.get_stats_contributors()

    commits_by_location = {}

    # stats will be a list of StatsContributor objects
    for contributor in stats:

        # there are cases where a contributor can't be found anymore
        if contributor.author:
            print(contributor.author.name, contributor.author.location)
        else:
            print("unknown person")

        print(contributor.total)



if __name__ == "__main__":
    repo_stats("brendan-w/python-OBD")
