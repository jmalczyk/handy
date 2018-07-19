#!/bin/bash
# Split a shapefile by attribute values.
# Usage: splitshp.sh shapefilename.shp some_field_name

IFS=$"\n"

if [[ -z "$1" || -z "$2" ]]; then
  echo "Usage: split_by_attr.sh some_shapefile_name.shp some_field_name"
else
   SHAPEFILE=$1
   DATASET=${SHAPEFILE/\.shp/}
   FIELD_NAME=$2
   ogr2ogr  -sql "SELECT DISTINCT $FIELD_NAME FROM $DATASET" -f 'CSV' temp.csv $SHAPEFILE
   for FIELD_VALUE in $(tail -n +2 temp.csv);
   do
      echo  Processing $FIELD_VALUE ...
      ogr2ogr -sql "SELECT * FROM $DATASET where $FIELD_NAME = '$FIELD_VALUE'" -f 'ESRI Shapefile' ${FIELD_VALUE/ /_}.shp $SHAPEFILE
   done
fi
rm temp.csv
