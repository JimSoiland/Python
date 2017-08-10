"""
This program will import the MapReduce framework. It will use
this framework to execute a map and reduce function set. The
mapper and reducer will perform matrix multiplication AxB.
Input JSON data (matrix.json) formatted as: 
[matrix name, i, j, value]

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
    #we know the dot product operations necessary to
    #create C and we will produce output tuples
    #with the coordinates of C as keys
    #matricies are index 0-4. If you didn't know
    #the dimensions up front, you'd need to 
    #make two passes over the file (getting dimensions, 
    #then processing)
    
    matrix = in_record[0]
    i = in_record[1]
    j = in_record[2]
    value = in_record[3]
    for num in range(0,5):
        if matrix=='a':
            mr.emit_intermediate((i,num), (matrix,j,value))
        else:
            mr.emit_intermediate((num,j), (matrix,i,value))

def reducer(key, matrix_tup):
    #here, perform the actual dot product
    dot_prod = 0
    i = key[0]
    j = key[1]
    for left in matrix_tup:
        if left[0]=='a':
            for right in matrix_tup:
                if right[0]=='b' and left[1]==right[1]:
                    dot_prod += left[2]*right[2]
    mr.emit((key[0], key[1],dot_prod))
        

# Do not modify below this line
# =============================
if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
