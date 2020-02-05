#!/usr/bin/env python3
"""generates a shapefile from a list of tile files"""

import argparse
import os
import sys
from osgeo import ogr, osr
from hyp3lib.asf_geometry import geotiff2polygon, geometry2shape


def tileList2shape(listFile, shapeFile):

  # Set up shapefile attributes
  fields = []
  field = {}
  values = []
  field['name'] = 'tile'
  field['type'] = ogr.OFTString
  field['width'] = 100
  fields.append(field)

  files = [line.strip() for line in open(listFile)]
  for fileName in files:
    print('Reading %s ...' % fileName)
    polygon = geotiff2polygon(fileName)
    tile = os.path.splitext(os.path.basename(fileName))[0]
    value = {}
    value['tile'] = tile
    value['geometry'] = polygon
    values.append(value)
  spatialRef = osr.SpatialReference()
  spatialRef.ImportFromEPSG(4326)

  # Write geometry to shapefiles
  geometry2shape(fields, values, spatialRef, False, shapeFile)


def main():
    """Main entrypoint"""

    # entrypoint name can differ from module name, so don't pass 0-arg
    cli_args = sys.argv[1:] if len(sys.argv) > 1 else None

    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description=__doc__,
    )
    parser.add_argument('file_list',
                        help='name of the tiles file list')
    parser.add_argument('shape_file',
                        help='name of the shapefile')
    args = parser.parse_args(cli_args)

    if not os.path.exists(args.file_list):
        print('GeoTIFF file (%s) does not exist!' % args.file_list)
        sys.exit(1)

    tileList2shape(args.file_list, args.shape_file)


if __name__ == '__main__':
    main()
