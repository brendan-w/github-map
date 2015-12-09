#!/usr/bin/env python3

import os
import sys
import json

GEOJSON_COUNTRIES = "countries.json"
FRAMES = 5

def main(stats_file, location_file, output_file):

    if not os.path.isfile(stats_file):
        print("stats-file '%s' was not found")
        exit(-1)

    if not os.path.isfile(location_file):
        print("location-file '%s' was not found")
        exit(-1)

    with open(GEOJSON_COUNTRIES, "r") as f:
        countries = json.loads(f.read())

    with open(stats_file, "r") as f:
        stats = json.loads(f.read())

    with open(location_file, "r") as f:
        locations = json.loads(f.read())


    for i in range(FRAMES):

        max_commits = 0

        # addition pass
        for country in countries["features"]:
            country_code = country["properties"]["ISO_A2"]
            country["properties"]["commits"] = 0

            for stat in stats:
                name = stat["author"]["login"]

                # add up the number of commits per country
                if locations[name] and \
                   "countryCode" in locations[name] and \
                   (locations[name]["countryCode"] == country_code):

                    # calculate the total commits for this window
                    weeks = stat["weeks"]
                    week_a = int(len(weeks) / FRAMES * i)
                    week_b = int(len(weeks) / FRAMES * (i + 1))
                    print("number of weeks per frame: %d" % (week_b - week_a))
                    frame_weeks = weeks[week_a:week_b]
                    total = sum([w["c"] for w in frame_weeks])
                    country["properties"]["commits"] += total

            if country["properties"]["commits"] > max_commits:
                max_commits = country["properties"]["commits"]

        # normalization pass
        if max_commits > 0:
            for country in countries["features"]:
                country["properties"]["commits"] /= max_commits

        print("max commits for a country, frame %d: %d" % (i, max_commits))

        # done, write the new map
        with open("%s.%d" % (output_file, i), "w") as f:
            f.write(json.dumps(countries))




if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: python by_time_countries.py <stats-file> <location-file> <output-file>")
        exit(-1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])
