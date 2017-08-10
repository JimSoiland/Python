"""
This program will import the MapReduce framework. It will use
this framework to execute a map and reduce function set. The
mapper and reducer are going return a unique list of
truncated DNA sequences. The sequences will be parsed
as a JSON input file (DNA.json) with the format: [Sequence ID: Sequence]

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
    mr.emit_intermediate(in_record[1][:-10], 1)

def reducer(key, sequence_count):
    # key: sequence
    mr.emit(key)

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
