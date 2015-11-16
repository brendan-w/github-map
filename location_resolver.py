
import os
from github import Github


class Location_Resolver:
    """
        Class for converting GitHub usernames into Lat/Long's

        Export the following env vars to your shell:
            GITHUB_MAP_USERNAME
            GITHUB_MAP_PASSWORD

        Eventually, this class may communicate with a datastore
        to avoid excessive GitHub API calls.
    """
    
    def __init__(self):
        self.cache = {}
        self.gh = Github(os.getenv("GITHUB_MAP_USERNAME", ""), \
                         os.getenv("GITHUB_MAP_PASSWORD", ""))

    def __call__(self, username):
        if username not in self.cache:
            self.cache[username] = self.lookup(username)

        return self.cache[username]

    def lookup(self, username):
        user = self.gh.get_user(username)
        location_str = user.location




if __name__ == "__main__":
    lr = Location_Resolver()
    print(lr("torvalds")) # should print out a lat-long tuple

