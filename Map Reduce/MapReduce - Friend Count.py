"""
This program will import the MapReduce framework. It will use
this framework to execute a map and reduce function set. The
mapper and reducer are going to count the number of friends for
listed pairs of friends. The documents will be parsed
as a JSON input file (friends.json)

MapReduce Framework:
JSON import and MapReduce class defined in another file. Contains functions for:
*MapReduce Constructor: initializes intermediate dict and result list
*emit_intermediates: takes arguments for key and value to fill the above intermediate dict
*emit: appends reduced key/value pairs to above result list
*execute: loads JSON file line-by-line and executes mapper for each line
    executes reducer for each intermediate
"""

import MapReduce
import sys


mr = MapReduce.MapReduce()

def mapper(in_record):
    mr.emit_intermediate(in_record[0], 1)

def reducer(key, friend_count):
    # key: friend
    friends = 0
    for f in friend_count:
        friends +=1
    mr.emit((key,friends))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
