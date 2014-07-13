from sys import stdin, stdout
import json
from optparse import OptionParser

parser = OptionParser(usage="""%prog [options]

Make JSON smaller by reducing precision of floating point values
and removing white space. Works great for GeoJSON!

Examples:
  cat input.json | python %prog --precision 2 > output.json
  python %prog --precision 2 input.json > output.json
  python %prog -p 2 input.json output.json""")

defaults = dict(precision=3)

parser.set_defaults(**defaults)

parser.add_option('-p', '--precision', dest='precision',
                  type='int', help='Digits of precision, default %(precision)d.' % defaults)




if __name__ == '__main__':
    options, args = parser.parse_args()
    
    #
    # Read!
    #
    input = len(args) and open(args[0]) or stdin
    data = json.load(input, parse_float=lambda x:round(float(x), options.precision))
    
    #
    # Write!
    #
    encoder = json.JSONEncoder(separators=(',', ':'))
    encoded = encoder.iterencode(data)
    
    format = '%.' + str(options.precision) + 'f'
    output = len(args) == 2 and open(args[1], 'w') or stdout
    
    for token in encoded:
        output.write(token)

