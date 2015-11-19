
import os
import requests
from github import Github
from urllib.parse import urlencode


class Location_Resolver:
    """
        Class for converting GitHub usernames into Lat/Long's

        Export the following env vars to your shell:
            GITHUB_MAP_USERNAME
            GITHUB_MAP_PASSWORD
            GEONAMES_USERNAME

        Eventually, this class may communicate with a datastore
        to avoid excessive GitHub API calls.
    """

    GEONAMES_API_URL = "http://api.geonames.org/search"
    GEONAMES_PARAMS = {
        "username": "",
        "type": "json",
        "maxRows": 1,
        "q":"",
    }

    def __init__(self):
        self.cache = {}
        self.gh = Github(os.getenv("GITHUB_MAP_USERNAME", ""), \
                         os.getenv("GITHUB_MAP_PASSWORD", ""))
        self.GEONAMES_PARAMS["username"] = os.getenv("GEONAMES_USERNAME", "")


    def __call__(self, username):
        if username not in self.cache:
            self.cache[username] = self.lookup(username)

        return self.cache[username]


    def lookup(self, username):
        user = self.gh.get_user(username)

        if not user.location:
            return None

        return self.resolve_location(user.location)


    def resolve_location(self, query):

        params = dict(self.GEONAMES_PARAMS)
        params["q"] = query
        url = self.GEONAMES_API_URL + "?" + urlencode(params)

        try:
            r = requests.get(url)
            return r.json()["geonames"][0]
        except:
            return None



if __name__ == "__main__":
    lr = Location_Resolver()
    print(lr("torvalds")) # should print out a lat-long tuple

