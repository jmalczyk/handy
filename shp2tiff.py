#!/usr/bin/python
import os, ogr, osr,  gdal, numpy, shutil
import sys, argparse



def main(args):

	pixel_size = args.resolution
	NoData_value = 0  #args.no_data


	srs = osr.SpatialReference()
	srs.SetWellKnownGeogCS('EPSG:4326')

	min_x = -180
	max_x = 180
	min_y = -90
	max_y = 90


	# Create the destination data source
	x_res = max(int((max_x - min_x) / pixel_size), 1)
	y_res = max(int((max_y - min_y) / pixel_size), 1)

	target_ds = gdal.GetDriverByName('GTiff').Create(
		os.path.join(os.getcwd(), args.outfile), x_res, y_res, 1, gdal.GDT_UInt16)
	target_ds.SetProjection(srs.ExportToWkt())
	target_ds.SetGeoTransform((min_x, pixel_size, 0, max_y, 0, -pixel_size))

	band = target_ds.GetRasterBand(1)
	band.SetNoDataValue(NoData_value)


	source = ogr.Open(os.path.join(os.getcwd(), args.infile))
	source_layer = source.GetLayer()

	print('Writing %s from %s at %s ' % (
		args.outfile, args.infile, args.resolution))
	# Rasterize

	gdal.RasterizeLayer(target_ds, [1], source_layer, options=[
		"ATTRIBUTE=%s" % args.attribute,
		"SPARSE_OK=TRUE",
		"COMPRESS=LZW"])

	print('Wrote %s' % args.outfile)
	del target_ds



if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--attribute',
		dest='attribute', default="OBJECTID", metavar='ATTRIBUTE', type=str,
	    help='an attribute to burn to raster')
	parser.add_argument('--src',
		dest='infile', metavar='INFILE', type=str,
		help='an attribute to burn to raster')
	parser.add_argument('--dest',
		dest='outfile', metavar='OUTFILE', type=str,
	    help='an attribute to burn to raster')
	parser.add_argument('--resolution',
		default=0.01, dest='resolution', metavar='OUTFILE', type=float,
	    help='an attribute to burn to raster')


	args = parser.parse_args()
	if args.infile and args.outfile:
		print os.path.join(os.getcwd(), args.outfile)
		main(args)
	else:
		print(parser.print_help())
