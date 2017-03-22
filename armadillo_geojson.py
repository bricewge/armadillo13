#!/usr/bin/env python3

import re
import sys
import click
import json
import os

import kml2geojson.main as m


@click.command(short_help="Convert KML to GeoJSON")
@click.option('-st', '--style-type', type=click.Choice(m.STYLE_TYPES), 
  default=None)
@click.option('-sf', '--style-filename', 
  default='style.json')
@click.argument('kml_path')
@click.argument('output_dir')
def k2g(kml_path, output_dir, style_type, style_filename):
    """
    Given a path to a KML file, convert it to a a GeoJSON FeatureCollection file and save it to the given output directory.

    If ``--style_type`` is specified, then also build a JSON style file of the given style type and save it to the output directory under the file name given by ``--style_filename``.
    """
    m.convert(kml_path, output_dir, False, style_type, style_filename)

    output = output_dir + "/" + os.path.splitext(kml_path)[0] + ".geojson"
    coordinatesInProperties(output)

def coordinatesInProperties(file_path):
    """
    Modify a GeoJSON file to add longitude and latitude in properties for each
    'Feature'.
    """
    fo = open(file_path, "r")
    content = json.load(fo)
    for entry in content["features"]:
        entry["properties"]["longitude"] = entry["geometry"]["coordinates"][0]
        entry["properties"]["latitude"] = entry["geometry"]["coordinates"][1]
    json.dump(content, open(file_path, "w"), indent=4)

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(k2g())
