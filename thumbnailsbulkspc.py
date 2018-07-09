#!/usr/local/bin/python3.5
from PIL import Image
import glob, os, sys

size   = 128, 128
type = sys.argv[1]
type = "spc"
print(type)


if type == 'spc':
	outdir = "/home/chariya/webapps/static_media/utils/images/spcthumb/"
	indir  = "/home/chariya/webapps/static_media/utils/images/species/"
elif type == "hyb":
	outdir = "/home/chariya/webapps/static_media/utils/images/hybthumb/"
	indir  = "/home/chariya/webapps/static_media/utils/images/hybrid/"
else:
	print("Need type parameter (spc or hyb)")
	exit

#outdir = "thumb/"
#indir = "download/"
	
i = 0
for infile in glob.glob(indir+"*.jpg"):
	i = i+1
	#if i%100==0: print(i)

#  Check if file exists
	fdir, fname = os.path.split(os.path.abspath(infile))
	file, ext   = os.path.splitext(fname)
	thumbname	= outdir+file+"_thumb.JPEG"
	if not os.path.exists(thumbname):
		img = Image.open(infile)
		width, height = img.size

		if width > height:
			delta = width - height
			left = int(delta/2)
			upper = 0
			right = height + left
			lower = height
		else:
			delta = height - width
			left = 0
			upper = int(delta/2)
			right = width
			lower = width + upper

		print(fname,"\n", thumbname)
		try:
			img = img.crop((left, upper, right, lower))
		except:
			print("bad image")
		img.thumbnail(size, Image.ANTIALIAS)
		img.save(thumbname)


