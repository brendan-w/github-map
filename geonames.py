
import os
from urllib.parse import urlencode
import requests


# Note: you will need to export the GEONAMES_USERNAME var from your shell


GEONAMES_API_URL = "http://api.geonames.org/search"
GEONAMES_PARAMS = {
    "username": os.getenv("GEONAMES_USERNAME", ""),
    "type": "json",
    "maxRows": 1,
    "q":"",
}



def get_lat_lng(query):

    params = dict(GEONAMES_PARAMS)
    params["q"] = query
    url = GEONAMES_API_URL + "?" + urlencode(params)

    try:
        r = requests.get(url)
        data = r.json()
        return (
            data["geonames"][0]["lat"],
            data["geonames"][0]["lng"]
        )
    except:
        return None


if __name__ == "__main__":
    print(get_lat_lng("Rochester NY"))

