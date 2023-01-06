import os, sys, glob, re, shutil, hashlib, urllib, zipfile
from time import sleep
import MySQLdb as mdb
import pyodbc, base64
from io import BytesIO
from PIL import Image
import unicodedata
import datetime
import urllib2
import urllib

os.environ["http_proxy"]='<proxy_url>'

def logit(logfile,caller,statement):
	log = open( logfile, 'a' )
	dtstamp = str(datetime.datetime.now())
	log.write(dtstamp + "|" + caller + "|" + statement + '\n')
	log.close
	print caller + "\t" + statement + "\n"

def getargs(debug):
	if debug == 1:
		print 'ss_functions: getargs'
	if len(sys.argv) == 1:
		print 'Choose environment to snapshot:\n'
		print '1) Development (GSWS environment yet enabled.  Will use tst)\n'
		print '2) Test\n'
		print '3) Production\n'
		u_in = raw_input("Enter 1, 2 or 3 (or q to quit): ")
		while u_in not in ['1','2','3','q']:
			print "Invalid Entry"
			u_in = raw_input("Enter 1, 2 or 3 (or q to quit): ")
	elif len(sys.argv) == 2:
		if str(sys.argv[1]) not in ['1','2','3','q']:
			print "Invalid commandline argument passed.  Valid entries are 1,2,3 or q.  Please check calling function:",str(sys.argv[0])
			print 'Hit return to exit'
			raw_input()
		else:
			u_in = str(sys.argv[1])
	else:
		print "Invalid use of commandline arguments.  Valid entries are 1,2,3 or q.  Please check calling function:",str(sys.argv[0])
		print 'Hit return to exit'
		raw_input()
		sys.exit()
	if u_in == '1':
		sstype = 'dev'
		baseurl = '<base_url_dev>'
		ssrepopath = '<dev_url>'
		conss = mdb.connect('localhost','root','<PW>','iggessdbdev')
		conbe = mdb.connect('localhost', 'root', '<PW>', 'iggebedbdev')
		print 'Development environment not yet defined.  Using tst environment for GSWService API calls'
		print 'Hit return to continue'
		raw_input()
	elif u_in == '2':
		sstype = 'tst'
		baseurl = '<base_url_test>'
		ssrepopath = '<test_url>'
		conss = mdb.connect('localhost','root','PW','iggessdbtst')
		conbe = mdb.connect('localhost', 'root', 'PW', 'iggebedbtst')
	elif u_in == '3':
		sstype = 'prd'
		baseurl = '<base_url_prod>'
		ssrepopath = '<prod_url>'
		conss = mdb.connect('localhost','root','<PW>','iggessdbprd')
		conbe = mdb.connect('localhost', 'root', '<PW>', 'iggebedbprd')
	elif u_in == 'q':
		print 'Operation canceled'
		print 'Hit return to exit'
		raw_input()
		sys.exit()
	else:
		print 'Invalid entry'
		print 'Hit return to exit'
		raw_input()
		sys.exit()
	return (sstype,baseurl,ssrepopath,conss,conbe)		

def getSSID(debug,conss,cursorss,ssdate,sstype):  #is this being used?
	if debug == 1:
		print 'ss_functions: getSSID'
	sql = "SELECT * FROM tblsnapshots WHERE ssdate=%s AND sstype=%s"
	args = (ssdate,sstype)
	cursorss.execute(sql,args)
	if cursorss.rowcount == 0:
		ssidentifier = 1
	else:
		ssidentifier = cursorss.rowcount + 1
	sql = "INSERT into tblsnapshots(ssdate,sstype,ssidentifier) VALUES(%s,%s,%s)"
	args = (ssdate,sstype,ssidentifier)
	cursorss.execute(sql,args)
	conss.commit()
	sql = "SELECT ssid FROM tblsnapshots Where ssdate=%s AND sstype=%s"
	args = (ssdate,sstype)
	cursorss.execute(sql,args)
	for (ssid) in cursorss:
		ssid = int(ssid[0])
	return (ssid,ssidentifier)	

def md5Checksum(debug,filePath):
	if debug == 1:
		print 'ss_functions: md5Checksum'
#	print 'filePath:',filePath
	BLOCKSIZE = 65536
	hasher = hashlib.md5()
	with open(filePath, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf)>0:
				hasher.update(buf)
				buf = afile.read(BLOCKSIZE)
#	print 'hash:',hasher.hexdigest()
	return hasher.hexdigest()

def getHWConfigurations(debug,baseurl):
	if debug == 1:
		print 'ss_functions: getHWConfigurations'
	url = baseurl + 'hwconfigurations'
	urllib2.install_opener(
		urllib2.build_opener(
			urllib2.ProxyHandler({'http': '<proxy_url>'})
		)
	)
	print 'url:',url
	response = urllib2.urlopen(url)
	try:
		response = urllib2.urlopen(url)
	except IOError, e:
		print 'first attempt failed.  trying again'
		try:
			response = urllib2.urlopen(url)
		except IOError, e:
			print 'second attempt faile.  Trying for last time.'
			try:
				response = urllib2.urlopen(url)
			except IOError, e:
				print 'Final attempt failed'
				return	
	tmpstr = response.read().split('},{')
	configs = []
	for str in tmpstr:
		str = str.replace('[{','')
		str = str.replace('}]','')
		tmpstr2 = str.split(',')
		for str2 in tmpstr2:
			str2 = str2.replace('"','')
			data = str2.split(':')
			if 'DeviceId' in data[0]:
				deviceid = data[1]
			elif 'FinishedDate' in data[0]:
				finisheddate = data[1]
			elif 'GraphicsBrand' in data[0]:
				graphicsbrand = data[1]
			elif 'GroupId' in data[0]:
				bucketid = data[1]
			elif 'LastUpdatedOn' in data[0]:
				lastupdatedon = data[1]
		tuple = (deviceid,bucketid,graphicsbrand,finisheddate,lastupdatedon)
		configs.append(tuple)
	return configs

def getGamesByDeviceId(debug,deviceid,baseurl):
	if debug == 1:
		print 'ss_functions: getGamesByDeviceId'
	url = baseurl + 'games/' + deviceid
	urllib2.install_opener(
		urllib2.build_opener(
			urllib2.ProxyHandler({'http': '<proxy_url>'})
		)
	)
	try:
		response = urllib2.urlopen(url)
	except IOError, e:
		print 'first attempt failed.  trying again'
		try:
			response = urllib2.urlopen(url)
		except IOError, e:
			print 'second attempt faile.  Trying for last time.'
			try:
				response = urllib2.urlopen(url)
			except IOError, e:
				print 'Final attempt failed'
				return
	tmpstr = response.read().split('},{')
	games = []
	for str in tmpstr:
		str = str.replace('[\'','')
		str = str.replace('\']','')
		tmpstr2 = str.split(',')
		for str2 in tmpstr2:
			str2 = str2.replace('":','|')
			str2 = str2.replace('"','')
			data = str2.split('|')
			if 'TaskId' in data[0]:
				taskid = data[1]
			elif 'SalesForceId' in data[0]:
				salesforceid = data[1]
			elif 'Name' in data[0]:
				name = data[1]
			elif 'LastUpdatedOn' in data[0]:
				lastupdatedon = data[1]
			elif 'Thumbnail' in data[0]:
				thumbnail = data[1]
			elif 'FinishedDate' in data[0]:
				finisheddate = data[1]
			elif 'ReleaseDate' in data[0]:
				releasedate = data[1]
		tuple = (taskid,salesforceid,name,lastupdatedon,finisheddate,releasedate,thumbnail)
		games.append(tuple)
	games_sorted = sorted(games, key=lambda tup: tup[0])
	return games_sorted

def getzipscreenshots(debug,tempzipdir,taskid,deviceid,baseurl):
	if debug == 1:
		print 'ss_functions: getzipscreenshots'
	fileList=os.listdir(tempzipdir)
	if len(fileList) > 0:
		for file in fileList:
			os.remove(tempzipdir + file)
	url = baseurl + 'games/DownloadImageZip/' + taskid + '/' + deviceid
#	proxy = {'http': '<proxy_url>'}
	name = os.path.join(tempzipdir, 'temp.zip')
	try:
		name, hdrs = urllib.urlretrieve(url, name)
	except IOError, e:
		print "Can't retrieve %r to %r: %s" % (url, tempzipdir, e)
		print 'trying for second time'
		try:
			name, hdrs = urllib.urlretrieve(url, name)
		except IOError, e:
			print 'Second attempt failed.  Trying one last time.'
			print "Can't retrieve %r to %r: %s" % (url, tempzipdir, e)
			try:
				name, hdrs = urllib.urlretrieve(url, name)
			except IOError, e:
				print 'Final attempt failed.'
				return
	try:
		z = zipfile.ZipFile(name)
	except zipfile.error, e:
		print "Bad zipfile (from %r): %s" % (url, e)
		return
	for n in z.namelist():
		dest = os.path.join(tempzipdir, n)
		destdir = os.path.dirname(dest)
		if not os.path.isdir(destdir):
			os.makedirs(destdir)
		data = z.read(n)
		f = open(dest, 'wb')
		f.write(data)
		f.close()
	z.close()
	sleep(1.0)
	# consider a while file exists loop and try except block for the os.unlink command.
	os.unlink(name)

def getGamesListWithConfig(debug,baseurl):
	if debug == 1:
		print 'ss_functions: getGamesListWithConfig'
	url = baseurl + '/games/GetGamesWithConfig'
	urllib2.install_opener(
		urllib2.build_opener(
			urllib2.ProxyHandler({'http': '<proxy_url>'})
		)
	)
	response = urllib2.urlopen(url)
	tmpstr = response.read().split('},{')
	configs = []
	for str in tmpstr:
		str = str.replace('[{','')
		str = str.replace('}]','')
		tmpstr2 = str.split(',')
		for str2 in tmpstr2:
			str2 = str2.replace('"','')
			data = str2.split(':')
			if 'TaskId' in data[0]:
				taskid = data[1]
		configs.append(taskid)
	return configs

def getConfig(debug,taskid,ssarchident,tempzipdir,baseurl):
	if debug == 1:
		print 'ss_functions: getConfig'
	fileList=os.listdir(tempzipdir)
	if len(fileList) > 0:
		for file in fileList:
			os.remove(tempzipdir + file)
	url = baseurl + 'games/DownloadConfigZip/' + taskid
	urllib2.install_opener(
		urllib2.build_opener(
			urllib2.ProxyHandler({'http': '<proxy_url>'})
		)
	)
	name = os.path.join(tempzipdir, 'temp.zip')
	try:
		name, hdrs = urllib.urlretrieve(url, name)
	except IOError, e:
		print "Can't retrieve %r to %r: %s" % (url, tempzipdir, e)
		print 'Attempting 2nd try'
		try:
			name, hdrs = urllib.urlretrieve(url, name)
		except IOError, e:
			print '2nd attempt failed.  Trying one last time'
			try:
				name, hdrs = urllib.urlretrieve(url, name)
			except IOError, e:
				print 'final attempt failed'
				return
	try:
		z = zipfile.ZipFile(name)
	except zipfile.error, e:
		print "Bad zipfile (from %r): %s" % (url, e)
		return
	for n in z.namelist():
		dest = os.path.join(tempzipdir, n)
		destdir = os.path.dirname(dest)
		if not os.path.isdir(destdir):
			os.makedirs(destdir)
		data = z.read(n)
		f = open(dest, 'wb')
		f.write(data)
		f.close()
	z.close()
	sleep(1.0)
	os.unlink(name)	
	
def loadDeviceIds(debug,conss,cursorss,ssid,configs):
	if debug == 1:
		print 'ss_functions: loadDeviceIds'
	for item in configs:
		deviceid = item[0]
		bucketid = item[1]
		sql = "SELECT ssdid FROM tblssdeviceids WHERE ssid=%s AND deviceid=%s AND bucketid=%s ORDER BY ssdid DESC"
		args = (ssid,deviceid,bucketid)
		cursorss.execute(sql,args)
		if cursorss.rowcount == 0:
			sql = "INSERT into tblssdeviceids(ssid,deviceid,bucketid) VALUES(%s,%s,%s)"
			args = (ssid,deviceid,bucketid)
			cursorss.execute(sql,args)
			conss.commit()
			sql = "SELECT ssdid FROM tblssdeviceids WHERE ssid=%s AND deviceid=%s AND bucketid=%s  ORDER BY ssdid DESC"
			args = (ssid,deviceid,bucketid)
			cursorss.execute(sql,args)
			if cursorss.rowcount == 0:
				print 'error creating deviceid record for deviceid:',deviceid,'bucketid:',bucketid
			elif cursorss.rowcount > 1:
				print 'Error:  multiple records found for deviceid:',deviceid,'bucketid:',bucketid
			else:
				print 'Added new record to tblssdeviceid for deviceid:',deviceid,'bucketid:',bucketid
		elif cursorss.rowcount >1:
			print 'ERROR:  Multiple matching records found for deviceid:',deviceid
	print "\n"
			
def getTitleId(debug,conss,cursorss,ssid,taskid,name,finisheddate,releasedate,salesforceid,lastupdatedon):	#Need to find out what lastupdateon is and add it below if needed
	if debug == 1:
		print 'ss_functions: getTitleId'
	sql = "SELECT sstitleid FROM tblsstitles WHERE taskid=%s AND ssid=%s ORDER BY sstitleid DESC"
	args = (taskid,ssid)
	cursorss.execute(sql,args)
	if cursorss.rowcount == 0:
		sql = "INSERT into tblsstitles(ssid,name,taskid,finisheddate,releasedate,salesforceid) VALUES(%s,%s,%s,%s,%s,%s)"
		args = (ssid,name,taskid,finisheddate,releasedate,salesforceid)
		cursorss.execute(sql,args)
		conss.commit()
		sql = "SELECT sstitleid FROM tblsstitles WHERE taskid=%s AND ssid=%s ORDER BY sstitleid DESC"
		args = (taskid,ssid)
		cursorss.execute(sql,args)
		if cursorss.rowcount == 0:
			print 'error creating title record for taskid:',taskid
			sstitleid = 0
		elif cursorss.rowcount > 1:
			print 'Error:  multiple records found for taskid:',taskid
			sstitleid = 0
		else:
			data = cursorss.fetchone()
			sstitleid = int(data[0])
	elif cursorss.rowcount > 1:
		print 'Multiple matching records found for title id.  Using the most recent'
		data = cursorss.fetchone()
		sstitleid = int(data[0])
	else:
		data = cursorss.fetchone()
		sstitleid = int(data[0])
	return sstitleid

def writethumbnail(debug,conss,cursorss,ssid,tmppath,ssrepopath,thumbnail,taskid,sstitleid,ssarchident,conbe,cursorbe):
	if debug == 1:
		print 'ss_functions: writethumbnail'
	have_thumbnail = 0
	fileList=os.listdir(tmppath)
	if len(fileList) > 0:
		for file in fileList:
			os.remove(tmppath + file)
	ssthmbdir = ssrepopath + 'thmbs\\'
	thmbname = str(taskid) + '.jpg'  #Temporary for chksum calc then to be renamed with archident when the file is archived.  save arch reference in advance.
	if not os.path.exists(ssthmbdir):
		os.makedirs(ssthmbdir)
	fi = open(tmppath + thmbname, 'wb')
	fi.write(thumbnail.decode('base64'))
	fi.close()
	new_chksum = md5Checksum(debug,tmppath + thmbname)
#  Consider looking for an existing file that may be a duplicate	
	if os.path.isfile(ssthmbdir+thmbname):
		if debug == 1:
			print '1:T'
		old_chksum = md5Checksum(debug,ssthmbdir+thmbname)
		if new_chksum == old_chksum: #will use the previous file and copy the reference into a new record and delete the new file.
			if debug == 1:
				print '2:T'
			os.remove(tmppath + thmbname)
			sql = "SELECT tblssthumbnails.ssthmbid,tblssthumbnails.ssarchident, tblsstitles.ssid \
								FROM tblssthumbnails \
								JOIN tblsstitles on tblssthumbnails.sstitleid = tblsstitles.sstitleid \
								WHERE ssthmbname=%s AND chksum=%s ORDER by ssid DESC"
			args = (thmbname,new_chksum)
			cursorss.execute(sql,args)
			if cursorss.rowcount == 0:
				if debug == 1:
					print '3:F'
				print 'Error:  Missing original record definition for thmbname:',thmbname
				sql = "INSERT into tblssthumbnails (sstitleid,ssthmbname,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
				args = (sstitleid,thmbname,ssarchident,new_chksum)
				cursorss.execute(sql,args)
				conss.commit()
				have_thumbnail = 1
			else:
				if debug == 1:
					print '3:T'
				data = cursorss.fetchone()
				if data[0] is None:
					ssthmbid = 0
				else:
					ssthmbid = data[0]
				if data[1] is None:
					p_ssarchident = 0
				else:
					p_ssarchident = data[1]
				if data[2] is None:
					p_ssid = 0
				else:
					p_ssid = data[2]
				sql = "SELECT thmb_chksum,thmb_vis_verified FROM tbltitles WHERE gameID=%s and thmb_chksum=%s"
				args = (taskid,new_chksum)
				cursorbe.execute(sql,args)
				if cursorbe.rowcount == 0:
					print 'Record not found in iggebedb for taskID:',taskid
					qa_chksum = 0
					qa_thmb_vis_verified = 0
					thmb_compares = 0
				else:
					data = cursorbe.fetchone()
					if data[0] is None:  #Forced to match process flow in screenshots where multiple files of same name can occur.
						qa_chksum = 0
					else:
						qa_chksum = data[0]
					if data[1] is None:
						qa_thmb_vis_verified = 0
					else:
						qa_thmb_vis_verified = data[1]
					if new_chksum == qa_chksum:
						thmb_compares = 1
					else:
						thmb_compares = 0
				if thmb_compares == 1:
					print 'thumbnail compares to BE database'
				else:
					print 'thumbnail does not compare to BE database'
				if qa_thmb_vis_verified == 1:
					print 'thumbnail previously visually verified'
				else:
					print 'thumbnail not previously visually verified'
				if p_ssid != ssid:
					if debug == 1:
						print '4:F'
					sql = "INSERT into tblssthumbnails (sstitleid,ssthmbname,ssarchident,chksum,vis_verified,compares) VALUES (%s,%s,%s,%s,%s,%s)"
					args = (sstitleid,thmbname,p_ssarchident,new_chksum,qa_thmb_vis_verified,thmb_compares)
					try:
						cursorss.execute(sql,args)
						conss.commit()
					except mdb.Error, e:
						print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
					have_thumbnail = 1
				else:
					if debug == 1:
						print '4:T'
					#  this will be an update, verify or overwrite?
					print 'Already have a current reference to thumbnail:',thmbname
					have_thumbnail = 1
					if ssthmbid != 0:
						sql = "UPDATE tblssthumbnails SET vis_verified=%s,compares=%s WHERE ssthmbid=%s"
						args = (qa_thmb_vis_verified,thmb_compares,ssthmbid)
						try:
							cursorss.execute(sql,args)
							conss.commit()
						except mdb.Error, e:
							print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
					else:
						print 'Error:  unable to find matching ssthmbid for sstitleid:',sstitleid,'thmbname:',thmbname
		else:  #chksum's are not the same
			if debug == 1:
				print '2:F'
			basename, extension = os.path.splitext(thmbname)
			if not os.path.exists(ssthmbdir + "\\archive\\"):
				os.makedirs(ssthmbdir + "\\archive\\")
			sql = "SELECT tblssthumbnails.ssthmbid,tblssthumbnails.ssarchident, tblsstitles.ssid \
								FROM tblssthumbnails \
								JOIN tblsstitles on tblssthumbnails.sstitleid = tblsstitles.sstitleid \
								WHERE ssthmbname=%s AND chksum=%s ORDER by ssid DESC"					
			args = (thmbname,old_chksum)
			cursorss.execute(sql,args)
			if cursorss.rowcount ==0:
				if debug == 1:
					print '5:F'
				print 'Error:  Unable to find tblssthumbnails entry for existing thumbnail:',thmbname,' Need to reconcile database'
				print 'Renaming existing file to archident:',ssarchident,'+_error and moving to archive directory'
				shutil.move(ssthmbdir + thmbname, ssthmbdir + "\\archive\\" + basename + "_" + archident + "_error" + extension)
			else:
				if debug == 1:
					print '5:T'
				data = cursorss.fetchone()
				p_archident = data[1]
				shutil.move(ssthmbdir + thmbname, ssthmbdir + "\\archive\\" + basename + "_" + archident + extension)
			shutil.move(tmppath + thmbname, ssthmbdir + thmbname)
			sql = "INSERT into tblssthumbnails (sstitleid,ssthmbname,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
			args = (sstitleid,thmbname,ssarchident,new_chksum)
			cursorss.execute(sql,args)
			conss.commit()
			have_thumbnail = 1
	else: #A previous version of the thumbnail does not exists.  copy in thumbnail and create a reference to it.
		if debug == 1:
			print '1:F'
		shutil.move(tmppath + thmbname, ssthmbdir + thmbname)
		sql = "INSERT into tblssthumbnails (sstitleid,ssthmbname,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
		args = (sstitleid,thmbname,ssarchident,new_chksum)
		cursorss.execute(sql,args)
		conss.commit()
		have_thumbnail = 1
	print 'have_thumbnail:',str(have_thumbnail)
	if have_thumbnail == 1:
		if debug == 1:
			print '6:T'
		sql = "UPDATE tblsstitles SET have_thumbnail=%s WHERE sstitleid=%s"
		args = (1,sstitleid)
		try:
			cursorss.execute(sql,args)
			conss.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	else:
		if debug == 1:
			print '6:F'
				
def getBenchmarkId(debug,conss,cursorss,sstitleid,bucketid,ssid):
	if debug == 1:
		print 'ss_functions: getBenchmarkId'
	sql = "SELECT ssbmid FROM tblssbenchmarks WHERE sstitleid=%s AND bucketid=%s AND ssid=%s ORDER BY ssbmid DESC"
	args = (sstitleid,bucketid,ssid)
	cursorss.execute(sql,args)
	if cursorss.rowcount == 0:
		sql = "INSERT into tblssbenchmarks(sstitleid,bucketid,ssid) VALUES(%s,%s,%s)"
		args = (sstitleid,bucketid,ssid)
		cursorss.execute(sql,args)
		conss.commit()
		sql = "SELECT ssbmid FROM tblssbenchmarks WHERE sstitleid=%s AND bucketid=%s AND ssid=%s ORDER BY ssbmid DESC"
		args = (sstitleid,bucketid,ssid)
		cursorss.execute(sql,args)
		if cursorss.rowcount == 0:
			print 'Error creating benchmark record for sstitleid:',sstitleid,'bucketid:',bucketid,'ssid:',ssid
			ssbmid = 0
		elif cursorss.rowcount > 1:
			print 'Error: multiple benchmark records found for sstitleid:',sstitleid,'bucketid:',bucketid,'ssid:',ssid,' after first finding none'
			ssbmnid = 0
		else:
			data = cursorss.fetchone()
			ssbmid = int(data[0])
	elif cursorss.rowcount > 1:
		print 'multiple benchmark records found for sstitleid:',sstitleid,'bucketid:',bucketid,'ssid:',ssid,'  Using most recent'
		data = cursorss.fetchone()
		ssbmid = data[0]
	else:
		data = cursorss.fetchone()
		ssbmid = int(data[0])		
	return ssbmid			

def processscreenshots(debug,conss,cursorss,ssbmid,sstitleid,tempzipdir,taskid,bucketid,sstype,ssdate,ssidentifier,ssrepopath,ssarchident,ssid,conbe,cursorbe):
	if debug == 1:
		print 'ss_functions: processscreenshots'
	ssrepodir = ssrepopath + 'ScreenShots\\' + str(taskid) + '\\' + str(bucketid) + '\\'
	if not os.path.exists(ssrepodir):
		os.makedirs(ssrepodir)
	fileList=os.listdir(tempzipdir)
	fileList.sort()	
	LfileList=os.listdir(ssrepodir)
	for Lfile in LfileList:
		if Lfile not in fileList and os.path.isfile(ssrepodir + Lfile):
			print 'file not retrieved from gsws API.  Archiving:', Lfile
			if not os.path.exists(ssrepodir + "\\archive\\"):
				os.makedirs(ssrepodir + "\\archive\\")
			basename, extension = os.path.splitext(Lfile)
			shutil.move(ssrepodir + Lfile, ssrepodir + 'archive\\' + basename + "_" + ssarchident + extension)	
	num_screenshots = 0
	compares = 0
	if len(fileList) > 0:
		for file in fileList:
			if debug == 1:
				print 'start main loop'
				print 'screenshot filename:', file
			basename, extension = os.path.splitext(file)
			new_chksum = md5Checksum(debug,tempzipdir + file)
# May want to add functionallity to check for a matching chksum in the database (but different target file)
			if os.path.isfile(ssrepodir + file):
				if debug == 1:
					print '1:T'
				old_chksum = md5Checksum(debug,ssrepodir + file)
				if new_chksum == old_chksum:  #will use the previous file and copy the reference into a new record and delete the new file.
					if debug == 1:
						print '2:T'
						print 'screenshot compares to existing'
					os.remove(tempzipdir + file)
					sql = "SELECT tblssscreenshots.ssbmid, tblssscreenshots.ssarchident, tblssbenchmarks.ssid \
								FROM tblssscreenshots \
									JOIN tblssbenchmarks ON tblssscreenshots.ssbmid = tblssbenchmarks.ssbmid \
									JOIN tblsstitles ON tblssbenchmarks.sstitleid = tblsstitles.sstitleid \
									WHERE tblssscreenshots.ssfilename=%s AND tblssscreenshots.chksum=%s AND tblsstitles.taskid=%s AND tblssbenchmarks.bucketid=%s \
									ORDER by ssid DESC"
					args = (file,new_chksum,taskid,bucketid)
					cursorss.execute(sql,args)
					if cursorss.rowcount == 0:
						if debug == 1:
							print '3:F'
#						print 'Error:  Missing original record definition for file:', file,'taskid:',taskid,'bucketid:',bucketid
						sql = "INSERT into tblssscreenshots (ssbmid,ssfilename,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
						args = (ssbmid,file,ssarchident,new_chksum)
						cursorss.execute(sql,args)
						conss.commit()
						num_screenshots = num_screenshots + 1
						compares = verifySS(debug,file,taskid,bucketid,new_chksum,conbe,cursorbe)
					else:
						if debug == 1:
							print '3:T'
						data = cursorss.fetchone()
						if data[1] is None:
							p_ssarchident = 0
						else:
							p_ssarchident = data[1]
						if data[2] is None:
							p_ssid = 0
						else:
							p_ssid = data[2]
						if p_ssarchident != 0:
							print 'screenshot originally recorded with archident:',p_ssarchident
						sql = "SELECT chksum, vis_verified FROM tblscreenshots \
								JOIN tblbenchmarks ON tblscreenshots.benchmarkID = tblbenchmarks.benchmarkID \
								WHERE gameID=%s and ssFilename=%s and bucketid=%s and chksum=%s"
						args = (taskid,file,bucketid,new_chksum)
						cursorbe.execute(sql,args)
						if cursorbe.rowcount == 0:
							print 'snapshot Record not found in iggebedb for taskID:',taskid, ', ssfilename:',file, ', bucketid:',bucketid
							qa_chksum = 0
							qa_vis_verified = 0
							ss_compares = 0
						elif cursorbe.rowcount > 1:
							print 'Error:  Multiple snapshot Records found in iggebedb for taskID:',taskid, ', ssfilename:',file, ', bucketid:',bucketid
							print 'Resolve issue.  setting vis_verified and ss_compares to 0'
							qa_chksum = 0
							qa_vis_verified = 0
							ss_compares = 0							
						else:
							data = cursorbe.fetchone()							
							if data[0] is None:  #Note:  This is forced since the query is already matching on chksum.  This is due to multiple platforms reporting into same bucket and filenames may be the same.
								qa_chksum = 0
							else:
								qa_chksum = data[0]
							if data[1] is None:
								qa_vis_verified = 0
							else:
								qa_vis_verified = data[1]
							if new_chksum == qa_chksum:
								ss_compares = 1
							else:
								ss_compares = 0
						if ss_compares == 1:
							print 'snapshot compares to BE database'
						else:
							print 'snapshot does not compare to BE database'
						if qa_vis_verified == 1:
							print 'snapshot previously visually verified'
						else:
							print 'snapshot not previously visually verified'
						if p_ssid != ssid:	
							if debug == 1:
								print '4:F'
							sql = "INSERT into tblssscreenshots (ssbmid,ssfilename,ssarchident,chksum,vis_verified,compares) VALUES (%s,%s,%s,%s,%s,%s)"
							args = (ssbmid,file,p_ssarchident,new_chksum,qa_vis_verified,ss_compares)
							cursorss.execute(sql,args)
							conss.commit()
							num_screenshots = num_screenshots + 1
#							compares = verifySS(debug,file,taskid,bucketid,new_chksum,conbe,cursorbe)
						else:
							if debug == 1:
								print '4:T'
							print 'current screenshot records exists.  No need to do anything'
							num_screenshots = num_screenshots + 1
				else:
					if debug == 1:
						print '2:F'
					if not os.path.exists(ssrepodir + "\\archive\\"):
						os.makedirs(ssrepodir + "\\archive\\")
					sql = "SELECT tblssscreenshots.ssbmid, tblssscreenshots.ssarchident, tblssscreenshots.vis_verified, tblssbenchmarks.ssid \
								FROM tblssscreenshots \
									JOIN tblssbenchmarks ON tblssscreenshots.ssbmid = tblssbenchmarks.ssbmid \
									JOIN tblsstitles ON tblssbenchmarks.sstitleid = tblsstitles.sstitleid \
									WHERE tblssscreenshots.ssfilename=%s AND tblssscreenshots.chksum=%s AND tblsstitles.taskid=%s AND tblssbenchmarks.bucketid=%s \
									ORDER by ssid DESC"
					args = (file,old_chksum,taskid,bucketid)
					cursorss.execute(sql,args)
					if cursorss.rowcount == 0:
						if debug == 1:
							print '5:F'
						print 'Error:  Unable to find screenshot entry for existing file:',file,'taskid:',taskid,'bucketid:',bucketid
						print 'renaming exising file to include ssarchident:',ssarchident,'_error and moving to archive directory'
						shutil.move(ssrepodir + file, ssrepodir + "\\archive\\" + basename + "_" + ssarchident + "_error" + extension)
					else:
						if debug == 1:
							print '5:T'
						data = cursorss.fetchone()
						archident = data[1]
						shutil.move(ssrepodir + file, ssrepodir + "\\archive\\" + basename + "_" + archident + extension)
					shutil.move(tempzipdir + file, ssrepodir + file)
					sql = "INSERT into tblssscreenshots (ssbmid,ssfilename,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
					args = (ssbmid,file,ssarchident,new_chksum)
					cursorss.execute(sql,args)
					conss.commit()						
					num_screenshots = num_screenshots + 1
					compares = verifySS(debug,file,taskid,bucketid,new_chksum,conbe,cursorbe)
			else:
				if debug == 1:
					print '1:F'
				shutil.move(tempzipdir + file, ssrepodir + file)
				sql = "INSERT into tblssscreenshots (ssbmid,ssfilename,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
				args = (ssbmid,file,ssarchident,new_chksum)
				cursorss.execute(sql,args)
				conss.commit()						
				num_screenshots = num_screenshots + 1
				compares = verifySS(debug,file,taskid,bucketid,new_chksum,conbe,cursorbe) #  Not needed assuming original file was not missing
			if compares == 1:
				print 'screenshot chksum compares to iggebedb chksum'
				sql = "UPDATE tblssscreenshots SET compares=1 WHERE ssfilename=%s AND ssbmid=%s"
				args = (file,ssbmid)
				try:
					cursorss.execute(sql,args)
					conss.commit()
				except mdb.Error, e:
					print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])	
	else:
		print 'No screenshots found for taskid:',taskid,' bucketid:',bucketid
	if num_screenshots > 0:
		if debug == 1:
			print '6:T'
		sql = "UPDATE tblssbenchmarks SET num_screenshots=%s WHERE ssbmid=%s"
		args = (num_screenshots,ssbmid)
		try:
			cursorss.execute(sql,args)
			conss.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])	
		sql = "UPDATE tblsstitles SET have_screenshot=%s WHERE sstitleid=%s"
		args = (1,sstitleid)
		try:
			cursorss.execute(sql,args)
			conss.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	else:
		if debug == 1:
			print '6:F'
	return num_screenshots

def processconfigs(debug,conss,cursorss,ssid,tempzipdir,ssrepopath,ssarchident,taskid):
	if debug == 1:
		print 'ss_functions: processconfigs'
	fileList=os.listdir(tempzipdir)
	fileList.sort()	
	num_configs = 0
	if len(fileList) > 0:
		num_configs = len(fileList)
		for file in fileList:
			if debug == 1:
				print 'start main loop'
			filename, tmpstr = file.split('__')
			taskid, bucketid, itr = tmpstr.split('_')
			shutil.move(tempzipdir + file, tempzipdir + filename)
			basename, extension = os.path.splitext(filename) 
			ssrepodir = ssrepopath + 'Configs\\' + str(taskid) + '\\' + str(bucketid) + '\\'			
			print 'filename:',filename
			print 'bucketid:',bucketid
			if not os.path.exists(ssrepodir):
				os.makedirs(ssrepodir)
			LfileList=os.listdir(ssrepodir)
			for Lfile in LfileList:
				Lfile_in_fileList = 0
				tmpLfile = Lfile + '__' + str(taskid) + '_' + str(bucketid)
				for file2 in fileList:	
					print 'file:',file2
					if file2.startswith(tmpLfile) and not os.path.isdir(ssrepodir + Lfile):
						Lfile_in_fileList = 1
				print 'Lfile_in_fileList:',Lfile_in_fileList
				if Lfile_in_fileList == 0 and not os.path.isdir(ssrepodir + Lfile):
					print 'Configuration file not found in new zip.  Archiving local file:',Lfile,'taskid:',taskid,'bucketid:',bucketid
					if not os.path.exists(ssrepodir + "archive\\"):
						os.makedirs(ssrepodir + "archive\\")
					lbasename, lextension = os.path.splitext(Lfile)
					shutil.move(ssrepodir + Lfile, ssrepodir + 'archive\\' + lbasename + "_" + ssarchident + lextension)					
			new_chksum = md5Checksum(debug,tempzipdir + filename)
#	Future:  check if there is a matching chksum in the db not associated with this benchmark
			if os.path.isfile(ssrepodir + filename):
				if debug == 1:
					print '1:T'
				old_chksum = md5Checksum(debug,ssrepodir + filename) 
				if new_chksum == old_chksum:
					if debug == 1:
						print '2:T'
					os.remove(tempzipdir + filename) 
					sql = "SELECT tblssconfigs.ssbmid, tblssconfigs.ssarchident, tblssconfigs.vis_verified, tblssbenchmarks.ssid \
								FROM tblssconfigs \
									JOIN tblssbenchmarks ON tblssconfigs.ssbmid = tblssbenchmarks.ssbmid \
									JOIN tblsstitles ON tblssbenchmarks.sstitleid = tblsstitles.sstitleid \
									WHERE tblssconfigs.configfilename=%s AND tblssconfigs.chksum=%s AND tblsstitles.taskid=%s AND tblssbenchmarks.bucketid=%s \
									ORDER by ssid DESC"
					args = (filename,new_chksum,taskid,bucketid)
					cursorss.execute(sql,args)
					if cursorss.rowcount == 0:
						if debug == 1:
							print '3:F'
						ssbmid = get_current_ssbmid(debug,conss,cursorss,ssid,bucketid,taskid)
						print 'ssbmid:',ssbmid
						vis_verified=0
						create_config_record(debug,conss,cursorss,ssbmid,filename,ssarchident,new_chksum,vis_verified)
						cursorss.execute(sql,args)
						conss.commit()
						if ssbmid != 0:
							if debug == 1:
								print '6:T'
							inc_num_configs(debug,conss,cursorss,ssbmid)
						else:
							if debug == 1:
								print '6:F'
					else:
						if debug == 1:
							print '3:T'
						data = cursorss.fetchone()
						p_ssarchident = data[1]
						vis_verified = data[2]
						p_ssid = data[3]
						if p_ssid != ssid:
							if debug == 1:
								print '4:F'
							ssbmid = get_current_ssbmid(debug,conss,cursorss,ssid,bucketid,taskid)
							print 'ssmbid:',ssbmid
							create_config_record(debug,conss,cursorss,ssbmid,filename,p_ssarchident,new_chksum,vis_verified)
							print 'ssbmid:',ssbmid
							print 'filename:',filename
							print 'p_ssarchident:',p_ssarchident
							print 'new_chksum:',new_chksum
							print 'vis_verified:',vis_verified
							cursorss.execute(sql,args)
							conss.commit()
							print 'ssbmid:',ssbmid
							if ssbmid != 0:
								if debug == 1:
									print '5:T'
								inc_num_configs(debug,conss,cursorss,ssbmid)
							else:
								if debug == 1:
									print '5:F'
						else:
							if debug == 1:
								print '4:T'
							print 'current config record exists.  Not taking any action.'
				else:
					if debug == 1:
						print '2:F'
					sql = "SELECT tblssconfigs.ssarchident FROM tblssconfigs \
								JOIN tblssbenchmarks ON tblssconfigs.ssbmid = tblssbenchmarks.ssbmid \
								JOIN tblsstitles ON tblssbenchmarks.sstitleid = tblsstitles.sstitleid \
									WHERE tblssconfigs.configfilename=%s AND tblssconfigs.chksum=%s AND tblsstitles.taskid=%s AND tblssbenchmarks.bucketid=%s \
									ORDER by ssid DESC"
					args = (filename,old_chksum,taskid,bucketid)
					cursorss.execute(sql,args)
					if not os.path.exists(ssrepodir + "\\archive\\"):
						os.makedirs(ssrepodir + "\\archive\\")
					if cursorss.rowcount == 0:
						if debug == 1:
							print '7:F'
						print 'Error:  Unable to find record for existing config filename:',filename,'taskid:',taskid,'bucketid:',bucketid
						print '        Changing existing filename to append this snapshot archident and .error and moving to archive folder'
						shutil.move(ssrepodir + filename, ssrepodir + "\\archive\\" + basename + "_" + ssarchident + extension + '.error')
					else:
						if debug == 1:
							print '7:T'
						data = cursorss.fetchone()
						archident = data[0]
						shutil.move(ssrepodir + filename, ssrepodir + "\\archive\\" + basename + "_" + archident + extension)
					shutil.move(tempzipdir + filename, ssrepodir + filename)
					ssbmid = get_current_ssbmid(debug,conss,cursorss,ssid,bucketid,taskid)
					print 'ssmbid:',ssbmid
					vis_verified=0
					create_config_record(debug,debug,conss,cursorss,ssbmid,filename,ssarchident,new_chksum,vis_verified)
					if ssbmid != 0:
						if debug == 1:
							print '8:T'
						inc_num_configs(debug,conss,cursorss,ssbmid)
					else:
						if debug == 1:
							print '8:F'
			else:
				if debug == 1:
					print '1:F'
				shutil.move(tempzipdir + filename, ssrepodir + filename)
				ssbmid = get_current_ssbmid(debug,conss,cursorss,ssid,bucketid,taskid)
				print 'ssbmid:',ssbmid
				vis_verified=0
				create_config_record(debug,conss,cursorss,ssbmid,filename,ssarchident,new_chksum,vis_verified)				
				if ssbmid != 0:
					if debug == 1:
						print '9:T'
					inc_num_configs(debug,conss,cursorss,ssbmid)
				else:
					if debug == 1:
						print '9:F'
			print '\n'
	else:
		print 'Error:  No configuration files found for taskid:',taskid
	if num_configs > 0:	
#		sql = "SELECT tblssbenchmarks.ssbmid FROM tblssbenchmarks \
#					JOIN tblsstitles ON tblssbenchmarks.sstitleid = tblsstitles.sstitleid \
#					WHERE tblssbenchmarks.ssid=%s AND tblssbenchmarks.bucketid=%s AND tblsstitles.taskid=%s "
#		args = (ssid,bucketid,taskid)
#		cursorss.execute(sql,args)
#		if cursorss.rowcount != 0:
#			print '21'
#			try:
#				cursorss.execute(sql,args)
#				conss.commit()
#			except mdb.Error, e:
#				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		sql = "UPDATE tblsstitles SET have_configs=%s WHERE taskid=%s AND ssid=%s"
		args = (1,taskid,ssid)
		try:
			cursorss.execute(sql,args)
			conss.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
#		else:
#			print '22'
#			print 'Error:  Unable to determine benchmark to apply num_configs for ssid:',ssid,'taskid:',taskid,'bucketid:',bucketid

def create_config_record(debug,conss,cursorss,ssbmid,filename,archident,chksum,vis_verified):
	if debug == 1:
		print 'ss_functions: create_config_record'
	sql = "INSERT into tblssconfigs (ssbmid,configfilename,ssarchident,chksum,vis_verified) VALUES (%s,%s,%s,%s,%s)"
	args = (ssbmid,filename,archident,chksum,vis_verified)
	cursorss.execute(sql,args)
	conss.commit()	
	
def get_current_ssbmid(debug,conss,cursorss,ssid,bucketid,taskid):
	if debug == 1:
		print 'ss_functions: get_current_ssbmid'
	sql = "SELECT tblssbenchmarks.ssbmid FROM tblssbenchmarks \
				JOIN tblsstitles ON tblssbenchmarks.sstitleid = tblsstitles.sstitleid \
				WHERE tblssbenchmarks.ssid=%s AND tblssbenchmarks.bucketid=%s AND tblsstitles.taskid=%s "
	args = (ssid,bucketid,taskid)
	cursorss.execute(sql,args)
	if cursorss.rowcount ==0:
		ssbmid = 0
		print 'Error:  missing ssbmid for taskid:',taskid,'bucketid:',bucketid,'ssid:',ssid
	else:
		data = cursorss.fetchone()
		ssbmid = data[0]
	return ssbmid
	
def inc_num_configs(debug,conss,cursorss,ssbmid):
	if debug == 1:
		print 'ss_functions: inc_num_configs'
	count = 0
	sql = "SELECT tblssbenchmarks.num_configs FROM tblssbenchmarks WHERE tblssbenchmarks.ssbmid=%s"
	args = (ssbmid)
	cursorss.execute(sql, [args])
	if cursorss.rowcount == 0:
		print 'Error:  missing ssbmid to update num_configs'
	else:
		data = cursorss.fetchone()
		count = int(data[0]) + 1
		print 'count:',count
		sql = "UPDATE tblssbenchmarks SET tblssbenchmarks.num_configs=%s WHERE tblssbenchmarks.ssbmid=%s"
		args = (count,ssbmid)
		try:
			cursorss.execute(sql,args)
			conss.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			
def verifySS(debug,file,taskid,bucketid,chksum,conbe,cursorbe):
	if debug == 1:
		print 'ss_functions: verifySS'
	compares = 0
	sql = 'SELECT chksum FROM tblscreenshots \
			JOIN tblbenchmarks ON tblscreenshots.benchmarkID = tblbenchmarks.benchmarkID \
			WHERE tblscreenshots.ssFilename=%s AND tblbenchmarks.gameID=%s AND tblbenchmarks.bucketID=%s'
	args = (file,taskid,bucketid)
	cursorbe.execute(sql,args)
	if cursorbe.rowcount == 0:
		print 'No matching screenshot was found in iggebedb.  ssfilename:',file,'taskid:',taskid,'bucketid:',bucketid
	else:
		data = cursorbe.fetchone()
		qadb_chksum = data[0]
		if chksum == qadb_chksum:
			compares = 1
	return compares
			
def comparedbs(debug,conss,cursorss,ssid):
	if debug == 1:
		print 'ss_functions: comparedbs'
	sql = "select  tblsstitles.name, tblsstitles.taskid, tblsstitles.releasedate, \
			tblssbenchmarks.ssbmid, tblssbenchmarks.bucketid, tblsstitles.have_thumbnail, \
			tblssbenchmarks.num_screenshots, tblssbenchmarks.num_configs \
			FROM tblssbenchmarks \
				JOIN tblsstitles ON tblssbenchmarks.sstitleid = tblsstitles.sstitleid \
            WHERE tblsstitles.ssid=%s \
			ORDER BY taskid ASC, bucketID ASC"
	args = (ssid)
	cursorss.execute(sql,[args])
	if cursorss.rowcount == 0:
		print 'No records returned'
	else:
		print 'num_records_returned',cursorss.rowcount
		data = cursorss.fetchall()
		for row in data:
			name = data[0]
			taskid = data[1]
			releasedate = data[2]
			ssbmid = data[3]
			bucketid = data[4]
			have_thumbnail = data[5]
			num_screenshots = data[6]
			num_configs = data[7]
			
