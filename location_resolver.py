
import os
import requests
from github import Github
from urllib.parse import urlencode



class Location:
    def __init__(self, geonames_data):
        """
            Loads all dictionary keys into same-named attributes

            Example input:

            {
                'population': 583776,
                'toponymName': 'Portland',
                'lng': '-122.67621',
                'countryName': 'United States',
                'fcode': 'PPLA2',
                'geonameId': 5746545,
                'adminName1': 'Oregon',
                'countryCode': 'US',
                'fcl': 'P',
                'fclName': 'city, village,...',
                'name': 'Portland',
                'fcodeName': 'seat of a second-order administrative division',
                'countryId': '6252001',
                'lat': '45.52345',
                'adminCode1': 'OR'
            }
        """

        # pull out the interesting bits
        # TODO: safe dict lookups
        self.raw = geonames_data
        self.lat = float(geonames_data["lat"])
        self.lng = float(geonames_data["lng"])
        self.name = str(geonames_data["name"])
        self.countryName = str(geonames_data["countryName"])
        self.countryCode = str(geonames_data["countryCode"])

    def __str__(self):
        return "%s %s" % (self.name, self.countryCode)

    def __eq__(self, other):
        return isinstance(other, Location) and (hash(self) == hash(other))

    def __hash__(self):
        return hash( (self.lat, self.lng) )



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

    def __init__(self, gh=None):
        """
            optionally pass your own github context
            (to save time, nothing more)
        """

        self.cache = {}
        self.GEONAMES_PARAMS["username"] = os.getenv("GEONAMES_USERNAME", "")

        if gh:
            self.gh = gh
        else:
            self.gh = Github(os.getenv("GITHUB_MAP_USERNAME", ""), \
                             os.getenv("GITHUB_MAP_PASSWORD", ""))


    def __call__(self, username, location_str=None):
        """
            Pass a lone username, and retrieve a dict of location information.

            OR

            If the location string (from the GitHub profile) is already known,
            pass it, and the resolver will cache/associate it with a GitHub
            username.
        """

        if username not in self.cache:
            self.cache[username] = self.lookup_username(username, location_str)

        return self.cache[username]


    def lookup_username(self, username, location_str=None):

        # if we don't have the GitHub location string, request it
        if not location_str:
            user = self.gh.get_user(username)
            location_str = user.location

            # if the user doesn't have any location info,
            # then there's nothing we can do
            if not location_str:
                return None

        return self.resolve_location_str(location_str)


    def resolve_location_str(self, location_str):
        """
            asks geonames to convert an abstract location string
            ("Rochester ny"), into a dict of common location info 
        """

        params = dict(self.GEONAMES_PARAMS)
        params["q"] = location_str
        url = self.GEONAMES_API_URL + "?" + urlencode(params)

        try:
            r = requests.get(url)
            data = r.json()["geonames"][0]
            # return Location(data) # emit a new Location object
            return data # emit raw JSON dict
        except:
            return None



if __name__ == "__main__":
    lr = Location_Resolver()
    print(lr("torvalds")) # should print out a dict of the user's location information
