#!/usr/bin/env python3

import os
import sys
import json
from location_resolver import Location_Resolver

def lookup_locations(stats_file, store_file):

    if not os.path.isfile(stats_file):
        print("stats-file '%s' was not found")
        exit(-1)

    try:
        with open(stats_file, "r") as f:
            stats = json.loads(f.read())
    except:
        print("failed to parse stats file")
        exit(-1)

    store = {} # key = GH username, value = GeoNames location

    # if we already have a store file, load it, and add to it
    if os.path.isfile(store_file):
        with open(store_file, "r") as f:
            store = json.loads(f.read())

    # get ready to look up locations
    lr = Location_Resolver()

    for stat in stats:
        username = stat["author"]["login"]
        if username not in store:
            print("looking up: %s" % username)
            store[username] = lr(username)
        else:
            print("skipping: %s" % username)

    # done, write the new store file
    with open(store_file, "w") as f:
        f.write(json.dumps(store, indent=4))




if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: python lookup_locations <stats-file> <store-file>")
        exit(-1)

    lookup_locations(sys.argv[1], sys.argv[2])
