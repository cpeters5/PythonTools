#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-
from __future__ import print_function
import urllib.request
import pymysql
from urllib.request import urlopen
from PIL import Image
import glob, os, sys

size   = 500, 400

conn = pymysql.connect(host='orchidroots.com', port=3306, user='chariya', passwd='imh3r3r3', db='orchidroots')
cur = conn.cursor()

#type = sys.argv[1]
type = "hyb"
print (type)
#dir = "C:/projects/orchids/bluenanta/utils/static/utils/images/"
dir = "/home/chariya/webapps/static_media/utils/images/"
if type == "spc":
	thumbdir = dir +"spiecies_thumb/"
	imgdir  = dir + "species/"
	stmthead = "UPDATE orchid_spcimages set image_file = '%s', width=%d, height=%d where id = %d"
	cur.execute("SELECT id, image_url, pid  FROM orchid_spcimages where image_url <>'' and image_url is not null and (image_file is null or image_file = '')")
else:
	thumbdir = dir + "hybrid_thumb/"
	imgdir  = dir + "hybrid/"
	stmthead = "UPDATE orchid_hybimages set image_file = '%s', width=%d, height=%d where id = %d"
	cur.execute("SELECT id, image_url, pid  FROM orchid_hybimages where image_url <>'' and image_url is not null and (image_file is null or image_file = '') and pid >= 0")
	
	
#print(cur.description)

#thumbdir = "thumb/"
#imgdir = "download/"

i = 0
for row in cur:
	i = i+1
	# if i >2:
		# break
	url = row[1]
	pid = row[2]
	if not url or url == '':
		#print ("Bad", url)
		cur.nextset()
	if not pid or pid == '':
		#print ("Bad", url)
		cur.nextset()
		
	fname = "%s_%09d_%09d.jpg" % (type,row[0],row[2])
	#print (fname)

	try:
		#print(url)
		#html = urlopen(url)
		local_filename, headers = urllib.request.urlretrieve(url,imgdir+fname)
			#print("True",url,html.read(),"\n")
		print(">>",local_filename,headers,"\n\n\n")
	except urllib.error.URLError as e:
		print("URLError -- ",row[0],e.reason)
		cur.nextset()
	except urllib.error.HTTPError as e:
		print("HTTPError -- ",row[0], e.reason)
		cur.nextset()

	img = Image.open(local_filename)
	width, height = img.size
	#print(width, height)
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

	try:
		img = img.crop((left, upper, right, lower))
	except:
		print("Bad data file - %s" % (fname))
	img.thumbnail(size, Image.ANTIALIAS)
	fdir, fname = os.path.split(os.path.abspath(local_filename))
	file, ext   = os.path.splitext(fname)
	img.save(thumbdir+file+".jpg")
	print(fdir,"\t",file)
	stmt = stmthead % (fname, width, height,row[0])
	curinsert = conn.cursor()

	curinsert.execute(stmt)
	conn.commit()
	#print (stmt)

	
cur.close()
conn.close()
