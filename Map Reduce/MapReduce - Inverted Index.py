"""
This program will import the MapReduce framework. It will use
this framework to execute a map and reduce function set. This
function set will take in arguments to create an "inverted index"
for keyword searching in documents. The documents will be parsed
as a JSON input file (books.json) for ease of use. The structure is <Doc_Name:Text>.

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
    # record key: document name
    # record value: document text
    key = in_record[0]
    #get a set of distinct tokens in the file by wrapping .split in set()
    words = set(in_record[1].split())
    #for every word, create an intermediate
    for w in words:
      mr.emit_intermediate(w, key)

def reducer(key, list_of_values):
    # key: word
    # value: document_name(s) associated with word
    doc_names = [] 
    # now reduce all those intermediates back down, buddy!
    for v in list_of_values:
      doc_names.append(v)
    mr.emit((key, doc_names))

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
