#!/usr/bin/env python3

import os
import sys
import json

GEOJSON_STATES = "states.json"

def main(stats_file, location_file, output_file):

    if not os.path.isfile(stats_file):
        print("stats-file '%s' was not found")
        exit(-1)

    if not os.path.isfile(location_file):
        print("location-file '%s' was not found")
        exit(-1)

    with open(GEOJSON_STATES, "r") as f:
        states = json.loads(f.read())

    with open(stats_file, "r") as f:
        stats = json.loads(f.read())

    with open(location_file, "r") as f:
        locations = json.loads(f.read())


    max_commits = 0

    # addition pass
    for state in states["features"]:
        state_name = state["properties"]["NAME"]
        state["properties"]["commits"] = 0

        for stat in stats:
            name = stat["author"]["login"]

            # add up the number of commits per state
            if locations[name] and \
               "countryCode" in locations[name] and \
               (locations[name]["countryCode"] == "US") and \
               locations[name]["adminName1"] == state_name:

                state["properties"]["commits"] += stat["total"]

        if state["properties"]["commits"] > max_commits:
            max_commits = state["properties"]["commits"]

    # normalization pass
    for state in states["features"]:
        state["properties"]["commits"] /= max_commits

    print("max commits for a state: %d" % max_commits)



    # done, write the new map
    with open(output_file, "w") as f:
        f.write(json.dumps(states))




if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python by_states <stats-file> <location-file> <output-file>")
        exit(-1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
