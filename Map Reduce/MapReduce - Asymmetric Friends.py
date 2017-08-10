"""
This program will import the MapReduce framework. It will use
this framework to execute a map and reduce function set. The
mapper and reducer are going to detect asymmetrical friendships 
(I am friends with you, but not vice versa). The documents will be parsed
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
    #the magic here is in a tricky representation of the keys...
    #create one key for each way the friendship *ought* to go
    #but only put the actual relationship pair into the data!
    mr.emit_intermediate(in_record[0], in_record)
    mr.emit_intermediate(in_record[1], in_record)

def reducer(key, relationships):
    # key: friend
    #value: relationships
    for o in relationships:
        if o[1] == key:
            found_match = False
            for i in relationships:
                if i[1] == o[0]:
                    found_match = True
            if found_match == False:
                mr.emit((key,o[0]))
                mr.emit((o[0],key))
# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
