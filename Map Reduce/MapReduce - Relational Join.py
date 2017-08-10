"""
This program will import the MapReduce framework. It will use
this framework to execute a map and reduce function set. The
mapper and reducer are going to do a relational join
on JSON presentations of order and item data. The documents will be parsed
as a JSON input file (records.json) for ease of use. JSON structure:
<(Source:Order Id),(data)>

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
    # record key: source,order_id
    # record value: everything else
    source = in_record[0]
    #get a set of distinct tokens in the file by wrapping .split in set()
    order_id = in_record[1]
    mr.emit_intermediate(order_id, in_record)

def reducer(key, record_list):
    # key: order_id
    # value: everything else
    for o in record_list:
        if o[0] == 'order':
            for i in record_list:
                if i[0] != o[0] and i[1] == o[1]:
                    mr.emit((o + i))
                else:
                    pass
        else:
            pass

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
