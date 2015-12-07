#!/bin/bash

curl https://api.github.com/repos/$1/$2/stats/contributors > data/$2.stats.json

./lookup_locations.py data/$2.stats.json data/$2.locations.json

./by_countries.py data/$2.stats.json data/$2.locations.json data/$2.countries.json

