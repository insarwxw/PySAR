#! /usr/bin/env python2
############################################################
# Program is part of PySAR v1.2                            #
# Copyright(c) 2017, Zhang Yunjun                          #
# Author:  Zhang Yunjun                                    #
############################################################


import sys
import os

import h5py
import numpy as np

import pysar._readfile as readfile
import pysar._writefile as writefile
import pysar._pysar_utilities as ut


def usage():
    print '''
usage:  range_distance.py  file  [outfile]

Generates range distance (in Radar Coordinate) for each pixel
  with required attributes read from the h5 file

input arguments:
  file    : string, input file name/path
  outfile : string, output file name/path for 2D incidence angle 
            calculated from file in radar coord

example:
  range_distance.py  velocity.h5
  range_distance.py  timeseries.h5
  range_distance.py  temporal_coherence.h5
    '''
    return

def main(argv):
    try:
        File = argv[0]
        atr = readfile.read_attribute(File)
    except:
        usage();  sys.exit(1)
    
    try:    outFile = argv[1]
    except: outFile = 'rangeDistance.h5'
    
    # Calculate look angle
    range_dis = ut.range_distance(atr, dimension=2)
    
    # Geo coord
    if 'Y_FIRST' in atr.keys():
        print 'Input file is geocoded, only center range distance is calculated: '
        print range_dis
        return range_dis

    # Radar coord
    else:
        print 'writing >>> '+outFile
        atr['FILE_TYPE'] = 'mask'
        atr['UNIT'] = 'm'
        writefile.write(range_dis, atr, outFile)
        return outFile

############################################################
if __name__ == '__main__':
    main(sys.argv[1:])





