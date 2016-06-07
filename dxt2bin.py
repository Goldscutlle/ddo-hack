#-------------------------------------------------------------------------------
# Name:        dxt2bin
# Purpose:     Converts base64 encoded chunks to binary data
#
# Author:      Marcus
#
# Created:     25/10/2015
# Copyright:   (c) Marcus 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import re
import os, sys
import struct
from struct import unpack, pack
import codecs
import binascii

def main():
    """
    this tool uses the base64 data generated by ddodxts to create binary files
    that can be pasted into DDS files to see the texture
    """
    a = "C:\\Program Files (x86)\\Turbine\\DDO Unlimited\\hack\\dxt-test.txt"
    b = "C:\\Program Files (x86)\\Turbine\\DDO Unlimited\\hack\\bin\\"
    infile = None
    outfile = None
    try:
        infile = open(a, 'r')
    except IOError:
        print "Error opening data file."
        exit()

    output = None
    line = infile.readline()
    while line <> "":
        fields = line.split(',')
        name = "%s.dxt" % fields[2]
        try:
            output = open("%s%s" % (b, name), 'wb')
            data = to_bin(fields)
            output.write(data)
        except IOError:
            print "Error writing data file."
            exit()
        output.close()
        line = infile.readline()

    infile.close()

def to_bin(fields):
    chunk = bytearray(0)
    header = bytearray(8)
    for n in range(len(fields[1])):
        header[n] = fields[1][n]
    header[n+1] = int(fields[4])
    chunk.extend(header)
    data1 = bytearray(binascii.a2b_base64(fields[5]))
    chunk.extend(data1)
    data2 = bytearray(binascii.a2b_base64(fields[6]))
    chunk.extend(data2)
    return chunk

def to_hex(t, nbytes):
    "Format text t as a sequence of nbyte long values separated by \\x."
    chars_per_item = nbytes * 2
    hex_version = binascii.hexlify(t)
    num_chunks = len(hex_version) / chars_per_item
    def chunkify():
        for start in xrange(0, len(hex_version), chars_per_item):
            yield hex_version[start:start + chars_per_item]
    return r'\x'.join(chunkify())

if __name__ == '__main__':
    main()