import os, sys, glob, re, shutil, hashlib
import MySQLdb as mdb
import pyodbc, base64
from io import BytesIO
from PIL import Image
import unicodedata
import datetime
import binascii
import inspect

conx = pyodbc.connect('DSN=DashBoard')
cursorx = conx.cursor()
platform_bucketed = ''

class Logger(object):
	def __init__(self, tracelog):
		self.terminal = sys.stdout
		self.log = open(tracelog, 'a')

	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)

def initapp(debug,dtstamp,dtstart,archstamp):
	if debug == 1:
		print 'be_functions: initapp'
		print 'sys.argv:',sys.argv
	if len(sys.argv) == 1:
		print 'Choose environment for which to gather backend data:\n'
		print '1) Development\n'
		print '2) Test\n'
		print '3) Production\n'
		u_in = raw_input("Enter 2 or 3 (or q to quit): ")
		while u_in not in ['1','2','3','q']:
			print "Invalid Entry 1"
			u_in = raw_input("Enter 2 or 3 (or q to quit): ")
		env = u_in
		print 'Is this a [n]ew run or [c]ontinuation of a previous run?'
		u_in = raw_input("Enter n or c (or q to quit): ")
		while u_in not in ['n','c','q']:
			print "Invalid Entry 2"
			u_in = raw_input("Enter n or c (or q to quit): ")
		exetype = u_in
	elif len(sys.argv) == 3:
		if str(sys.argv[1]) not in ['1','2','3','q']:
			print "Invalid commandline argument passed.  Valid entries are 1,2,3 or q.  Please check calling function:",str(sys.argv[0])
			print 'Hit return to exit'
			raw_input()
		else:
			env = str(sys.argv[1])
		if str(sys.argv[2]) not in ['n','c','q']:
			print "Invalid commandline argument passed.  Valid entries are [1,2,3 or q] followed by [n,c or q]. ex.  <...>> 1 n"
			print "Please check calling function:",str(sys.argv[0])
		else:
			exetype = str(sys.argv[2])
	else:
		print "Invalid use of commandline arguments.  Valid entries are [1,2,3 or q] followed by [n,c or q]. ex.  <...>> 1 n"
		print "Please check calling function:",str(sys.argv[0])
		print 'Hit return to exit'
		raw_input()
		sys.exit()
	print 'env:',env
	print 'exetype:',exetype
	if env == '1':
		environ = 'Dev'
		berepopath = 'D:\\Projects\\IGGE\\repo\\BERepo\\Dev\\'
		conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
	elif env == '2':
		environ = 'Test'
		berepopath = 'D:\\Projects\\IGGE\\repo\\BERepo\\Test\\'
		conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbtst')

	elif env == '3':
		environ = 'Prod'
		berepopath = 'D:\\Projects\\IGGE\\repo\\BERepo\\Prod\\'
		conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbprd')
	elif env == 'q':
		print 'Operation canceled'
		print 'Hit return to exit'
		raw_input()
		sys.exit()
	else:
		print 'Invalid entry 3'
		print 'Hit return to exit'
		raw_input()
		sys.exit()
	completedfile = 'D:\\Projects\\IGGE\\python_scripts\\backend\\script_collateral\\' + environ + '\\completed.txt'
	excludefile = 'D:\\Projects\\IGGE\\python_scripts\\backend\\script_collateral\\' + environ + '\\exclude.txt'
	logpath = 'D:\\Projects\\IGGE\\logfiles\\backend\\' + environ + '\\' + archstamp + '\\'
	if not os.path.exists(logpath):
		os.makedirs(logpath)
	tracelog = logpath + 'tracelog.txt'
	errlog = logpath + 'errlog.txt'
	chglog = logpath + 'chglog.txt'
	actlog = logpath + 'actlog.txt'
	logfiles = {'tracelog':tracelog,'errlog':errlog,'chglog':chglog,'actlog':actlog}
	for file in logfiles:
		if not os.path.isfile(file):
			open(file, 'w+').close()
	sys.stdout = Logger(tracelog)
	print "Begin run:", str(dtstart)
	print '\n'
	print 'Environment:',env
	print 'Execution type:',exetype
	print '\n'
	print 'Logfiles located at:', logpath, '{tracelog.txt,errlog.txt,chglog.txt}'
	print '\n'
	if exetype == 'n':
		if os.path.isfile(completedfile):
			os.remove(completedfile)
		cfile = open(completedfile,'w')
		cfile.close
	elif exetype == 'c':
		print 'Continuation of previous run.  Leaving completed.txt alone.'
		if not os.path.isfile(completedfile):
			print 'Error:  continuation requested, but no completed file list is present.  Create a new (blank) one.'
			cfile = open(completedfile,'w')
			cfile.close
	elif exetype == 'q':
		print 'Operation canceled'
		print 'Hit return to exit'
		raw_input()
		sys.exit()
	else:
		print 'Invalid entry 4'
		print 'Hit return to exit'
		raw_input()
		sys.exit()
	if os.path.isfile(excludefile):
		f = open(excludefile)
		lines = f.readlines()
		excludes = [str(e.strip()) for e in lines]
		if len(excludes) == 0:
			print 'Nothing specified in exclude file.  Nothing will be excluded.'
		else:
			print 'The following files will be excluded:'
			for exclude in excludes:
				print '\t'+str(exclude)
	else:
		print 'No exclude file found.  Creating empty file.'
		efile = open(excludefile,'w')
		efile.close
	print '\n'
	return (berepopath,conbe,completedfile,excludefile,logfiles)		

def md5Checksum(debug,filePath):
	if debug == 1:
		print 'be_functions: md5Checksum'
	BLOCKSIZE = 65536
	hasher = hashlib.md5()
	with open(filePath, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf)>0:
				hasher.update(buf)
				buf = afile.read(BLOCKSIZE)
	print '\t' + str(hasher.hexdigest())
	return hasher.hexdigest()

def logit(debug,logfiles,caller,statement):
#	print 'inspect:',inspect.stack()
#	print 'logfiles:',logfiles
	if debug == 1:
		print "be_functions: logit:", caller, statement
	for file in logfiles:
		log = open(file, 'a' )
		dtstamp = str(datetime.datetime.now())
		log.write(dtstamp + "|" + caller + "|" + statement + '\n')
		log.close		

def get_gsws_games_list(debug,logfiles):
	if debug == 1:
		print 'be_functions: get_gsws_games_list'
	sqlx = "SELECT DISTINCT TaskName FROM GswsResults"
	cursorx.execute(sqlx)
	rows = cursorx.fetchall()
	if len(rows) == 0:
		logstr = 'No games returned from GSWSResults view'
		logit(debug,[logfiles['actlog'],logfiles['errlog']],"get_gsws_games_list",logstr)
	else:
		logstr = str(len(rows)) + ' games returned from GSWSResults view'
		logit(debug,[logfiles['actlog']],"get_gsws_games_list",logstr)
	return rows

def get_taskId_gsws(debug,logfiles,TaskName):
	if debug == 1:
		print 'be_functions: get_taskID_gsws'
	sqlx = 'SELECT COUNT(DISTINCT TaskId) FROM GswsResults WHERE TaskName=?'
	argsx = (TaskName)
	cursorx.execute(sqlx,argsx)
	result = cursorx.fetchone()
	num_rows = result[0]
	sqlx = 'SELECT DISTINCT TaskName, TaskId, FinishedDate FROM GswsResults WHERE TaskName=? ORDER BY FinishedDate DESC'
	argsx = (TaskName)
	rows = cursorx.execute(sqlx,argsx)
	if num_rows == 0:
		logstr = 'No results found in GswsResults view for taskName: ' + TaskName
		logit(debug,[logfiles['actlog']], "get_taskId_gsws",logstr)
		TaskId = 0
	else:
		if num_rows > 1:
			logstr = 'Multiple results found in GswsResults view for taskName: ' + TaskName + '  Choosing most recent'
			logit(debug,[logfiles['actlog']], "get_taskId_gsws",logstr)
		result = cursorx.fetchone()
		TaskId = result[1]
	return TaskId		

def get_titleID_iggeqadb(debug,logfiles,con,cursor,TaskId,TaskName):
	if debug == 1:
		print 'be_functions: get_titleID_iggeqadb'
	sql = "SELECT titleID, name FROM tblTitles WHERE name=%s AND gameID=%s"
	args = ([TaskName],TaskId)
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	if cursor.rowcount == 0:
		print 'TaskName not found in iggeqadb.tblTitles:', TaskName
		sql = "INSERT into tblTitles(name,gameID) VALUES(%s,%s)"
		args = (TaskName,TaskId)
		try:
			cursor.execute(sql, args)
			con.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	elif cursor.rowcount > 1:
		logstr = "multiple records found in iggegadb.tblTitles for TaskName: " + TaskName
		logit(debug,[logfiles['actlog']], "get_titleID_iggeqadb",logstr)
	sql = "SELECT titleID FROM tblTitles Where name=%s AND gameID=%s"
	args = (TaskName,[TaskId])
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	if cursor.rowcount == 0:
		logstr = "No records found in tblTitles for gameID: " + TaskId
		logit(debug,[logfiles['actlog']], "get_titleID_iggeqadb", logstr)
		titleId = 0
	elif cursor.rowcount > 1:
		logstr = "Multiple records found in iggeqadb.tblTitles for TaskId:",TaskId,"TaskName:",TaskName
		logit(debug,[logfiles['actlog']], "get_titleID_iggeqadb", logstr)
		titleID = 0
	else:
		for (titleID) in cursor:
			titleId = int(titleID[0])
	return (titleId)	

def get_platform_list(debug,logfiles,TaskId):
	if debug == 1:
		print 'be_functions: get_platform_list'
	sqlx = 'SELECT DISTINCT RecommendedRootPath, BucketId, BucketName FROM GswsResults WHERE TaskId=?' #Note:  removed DeviceId from this query since it resulted in much duplication.
	argsx = (TaskId)
	cursorx.execute(sqlx,argsx)
	rows = cursorx.fetchall()
	return rows		

def	get_platformID_iggeqadb(debug,logfiles,con,cursor,platform,bucketId,bucketName):
	if debug == 1:
		print 'be_functions: get_platformID_iggeqadb'
	sql = "SELECT platformID,bucketID,bucketName FROM tblPlatforms WHERE description=%s"
	args = ([platform])
	cursor.execute(sql, args)
	if cursor.rowcount == 0:
		logstr = 'Platform not found in iggeqadb.tblPlatforms:', platform
		logit(debug,[logfiles['actlog']],"get_platformID_iggeqadb",logstr)
		sql = "INSERT into tblPlatforms(description) VALUES(%s)"
		args = ([platform])
		try:
			cursor.execute(sql, args)
			con.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		bucketed = "No"
		sql = "SELECT platformID FROM tblPlatforms WHERE description=%s"
		args = ([platform])
		cursor.execute(sql, args)
		data = cursor.fetchone()
		platformID = data[0]
	else:
		for (data) in cursor:
			if (str(bucketId)==data[1]) and (bucketName==data[2]):
				platformId = int(data[0])
				bucketed = "Yes"
			else:
				platformId = 0
				bucketed = "No"
				logstr ="Platform is not bucketed: " + platform
				logit(debug,[logfiles['actlog']], "get_platformID_iggeqadb", logstr)
	return (platformId,bucketed,bucketId,bucketName)	

def get_labId_iggeqadb(debug,logfiles,con,cursor,labname):
	if debug == 1:
		print 'be_functions: get_labId_iggeqadb'
	sql = "SELECT labId FROM tbllabs WHERE labName=%s"
	args = ([labname])
	cursor.execute(sql,args)
	if cursor.rowcount == 0:
		logstr = "No records found in iggeqadb.tbllabs for labname: " + labname
		logit(debug,[logfiles['actlog']], "get_labID_iggeqadb", logstr)
		labId = 0
	elif cursor.rowcount > 1:
		logstr = "Multiple records found in iggeqadb.tbllabs forlabname: " + labname
		logit(debug,[logfiles['actlog']], "get_labID_iggeqadb", logstr)
		labId = 0
	else:
		for (data) in cursor:
			labId = int(data[0])
	return(labId)	

def get_benchmarkID(debug,logfiles,con,cursor,labID,titleID,gameID,platformID):
	if debug == 1:
		print 'be_functions: get_benchmarkID'
	sql = "SELECT benchmarkID FROM tblBenchmarks WHERE labID=%s AND titleID=%s AND platformID=%s"
	args = (labID,titleID,platformID)
	cursor.execute(sql, args)
	if cursor.rowcount == 0:
		sql = "INSERT into tblBenchmarks(labID,titleID,gameID,platformID) VALUES(%s,%s,%s,%s)"
		args = (labID,titleID,gameID,platformID)
		cursor.execute(sql, args)
		con.commit()
	elif cursor.rowcount > 1:
		logstr = "multiple benchmards found"
		logit(debug,[logfiles['actlog']],"get_benchmarkID",logstr)
	sql = "SELECT benchmarkID FROM tblBenchmarks WHERE labID=%s AND titleID=%s AND platformID=%s" 
	args = (labID,titleID,platformID)
	cursor.execute(sql, args)
	for (benchmarkID) in cursor:
		benchmarkID = int(benchmarkID[0])
	return benchmarkID	

def get_dashboard_data(debug,logfiles,con,cursor,gameID, benchmarkID, platformID, platform_bucketed,archstamp,l_path_base,titleId):
	if debug == 1:
		print 'be_functions: get_dashboard_data'
	sqlx = 'SELECT DISTINCT TaskGuid,TaskName, SalesForceID, FinishedDate, ReleaseDate  FROM GswsResults WHERE TaskID=?'
	parmsx = (gameID)
	cursorx.execute(sqlx,parmsx)
	have_DashBoardEntry = ''
	if cursorx.rowcount == 0:
		have_DashBoardEntry = "No"
		TaskGuid = 'None'
		TaskName = 'None'
		SalesForceID = 'None'
		FinishedDate = 'None'
		ReleaseDate = 'None'
	else:
		have_DashBoardEntry = "Yes"
		for data in cursorx:
			TaskGuid = data[0]
			TaskName = data[1]
			SalesForceID = data[2]
#			GraphicsBrand = unicodedata.normalize('NFKD',data[6]).encode('ascii','ignore')
			FinishedDate = data[3]
			ReleaseDate = data[4]
	sql = "UPDATE tblTitles SET taskguid=%s, \
				salesforceid=%s, \
				finisheddate=%s, \
				releasedate=%s \
				WHERE gameID=%s"
	args = (TaskGuid,SalesForceID,FinishedDate,ReleaseDate,gameID)
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	if have_DashBoardEntry == 'No':
		logstr = 'No DashBoard Entry for:  ' + str(gameID)
		logit(debug,[logfiles['actlog']],"get_dashboard_data",logstr)
		gname = 'None'
	else:
		sqlx = 'SELECT Thumbnail FROM GswsResults WHERE TaskID=?'
		parmsx = (gameID)
		cursorx.execute(sqlx,parmsx)
		if cursorx.rowcount == 0:
			logstr = 'No Thumbnail found for:  ' + str(gameID)
			logit(debug,[logfiles['actlog']],"get_benchmarkID",logstr)
			have_thumbnail = 0
			thumbnail = 'none'
		else:
			have_thumbnail = 1
			data = cursorx.fetchone()
			bthumbnail = bytearray(data[0])
			thumbnail = binascii.b2a_base64(bthumbnail)
		sql = "UPDATE tblTitles SET have_thumbnail=%s WHERE gameID=%s"
		args = (have_thumbnail,gameID)
		try:
			cursor.execute(sql, args)
			con.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		if platform_bucketed == "Yes":
			sql = "SELECT bucketid,bucketname FROM tblplatforms WHERE platformID=%s"
			args = ([platformID])
			try:
				cursor.execute(sql, args)
				con.commit()
			except mdb.Error, e:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			if cursor.rowcount == 0:
				logstr = 'No platform found, though bucketed is yes.  platformID: ' + str(platformID)
				logit(debug,[logfiles['actlog'],logfiles['errlog']],"get_dashboard_data",logstr)
			else:
				for data in cursor:
					bucketid = data[0]
					bucketname = data[1]
				sqlx = 'SELECT DISTINCT TaskName, BucketId, BucketName, RecommendedRootPath FROM GswsResults WHERE TaskID=? AND BucketId=?'
				parmsx = (gameID,bucketid)
				cursorx.execute(sqlx,parmsx)
				if cursorx.rowcount == 0:
					logstr = 'No DashBoard Bucket Information for:  ' + str(gameID) + ' platformId: ' + str(platformID)
					logit(debug,[logfiles['actlog'],logfiles['errlog']],"get_dashboard_data",logstr)						
				else:
					for data in cursorx:
						rrp = data[3]
					sql = "UPDATE tblBenchmarks SET bucketid=%s, \
							bucketname=%s, \
							recommendedrootpath=%s \
							WHERE benchmarkID=%s"
					args = (bucketid, bucketname, rrp,[benchmarkID])
					try:
						cursor.execute(sql, args)
						con.commit()
					except mdb.Error, e:
						print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])				
		else:
			logstr = 'Platform not assigned bucketing information:  ' + str(platformID)
			logit(debug,[logfiles['actlog']],"get_dashboard_data",logstr)
			sql = "UPDATE tblBenchmarks SET recommendedrootpath='Unknown' WHERE benchmarkID=%s"
			args = ([benchmarkID])
			try:
				cursor.execute(sql, args)
				con.commit()
			except mdb.Error, e:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])	
		gname = test_gname(debug,logfiles,con,cursor,TaskName,titleId)
		if have_thumbnail == 1:
			thmb_path = l_path_base + '\\' + gname + '\\RTM\\' + str(gameID) + '\\thumbnail\\'
			write_thumbnail(debug,logfiles,con,cursor,thumbnail,thmb_path,gameID,archstamp)
	print '\tgname:',gname
	return gname	

def test_gname(debug,logfiles,con,cursor,gname,titleId):
	if debug == 1:
		print 'be_functions: test_gname'
	if gname.find(':') or gname.find('/'):
		for ch in [':','/']:
			if ch in gname:
				gname = gname.replace(ch,"")
				logstr = 'directory name for ' + gname + ' modified from original to remove special character'
				logit(debug,[logfiles['actlog']],"test_gname",logstr)
	sql = "UPDATE tbltitles SET alias=%s WHERE titleID=%s"
	args = (gname,titleId)
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])	
	return gname	

def get_paths_iggeqadb(debug,logfiles,con,cursor,labId):
	if debug == 1:
		print 'be_functions: get_paths_iggeqadb'
	sql = "SELECT vcFileShare FROM tbllabs WHERE labID=%s"
	args = ([labId])
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	if cursor.rowcount == 0:
		logstr = 'Error: No lab found for labId: ' + str(labId)
		logit(debug,[logfiles['actlog']],"get_paths_iggeqadb",logstr)
		r_path = ''
	elif cursor.rowcount > 1:
		logstr = 'Error: Multiple labs found for labId: ' + str(labId)
		logit(debug,[logfiles['actlog']],"get_paths_iggeqadb",logstr)
		r_path = ''
	else:
		for data in cursor:
			r_path = data[0]
	print '\tr_path:',r_path
	return(r_path)

def get_files(debug,logfiles,con,cursor,r_path,l_path,ftype,benchmarkID,archstamp):
	if debug == 1:
		print 'be_functions: get_files'
	if ftype == 'screenshot':
		table = 'tblScreenShots'
	elif ftype == 'config':
		table = 'tblconfigs'
	else:
		table = 'unknown'
	if not os.path.exists(r_path):
		if debug == 1:
			print '1:F'
		logstr = "Remote path does not exist:  " + r_path + "  benchmarkID:  " + str(benchmarkID)
		logit(debug,[logfiles['actlog'],logfiles['errlog']],"get_files",logstr)
	else:
		if debug == 1:
			print '1:T'
		if not os.path.exists(l_path):
			if debug == 1:
				print '2:F'
			os.makedirs(l_path)
		else:
			if debug == 1:
				print '2:T'
		fileList=os.listdir(r_path)  #file and fileList reference the remote directory
		fileList.sort()
		LfileList=os.listdir(l_path)
		for Lfile in LfileList:
			if Lfile not in fileList and os.path.isfile(l_path + Lfile):
				if debug == 1:
					print '3:F'
				print 'local ' + ftype + ' file not found in remote repository.  Archiving:', Lfile
				if not os.path.exists(l_path + "\\archive\\"):
					if debug == 1:
						print '4:F'
					os.makedirs(l_path + "\\archive\\")
				else:
					if debug == 1:
						print '4:T'
				basename, extension = os.path.splitext(Lfile)
				archfile = l_path + 'archive\\' + basename + "_" + archstamp + extension
				shutil.move(l_path + Lfile, archfile)
				logstr = 'Orphaned file found in ' + ftype + ' directory and moved to archive:  ' + archfile
				logit(debug,[logfiles['actlog'],logfiles['chglog']],"get_files",logstr)
			else:
				if debug == 1:
					print '3:T'
		n = 0
		if debug == 1:
			print 'Entering main loop of get_files for files of type:', ftype, 'benchmarkID:', benchmarkID, 'Total files to iterate:', len(fileList)
		if len(fileList) > 0:
			if debug == 1:
				print '5:T'
			for file in fileList:
				if debug == 1:
					print 'Top of main loop.  processing ' + ftype + ' file:', file
				if os.path.isfile(r_path + file) and file != 'Thumbs.db':
#				if os.path.isfile(r_path + file) and file.lower().endswith(('.jpg','.jpeg','.bmp','.png')): # and file.lower() != 'gameplay.jpg':
					if debug == 1:
						print '6:T'
					if file.lower() == 'gameplay.jpg':
						print 'Found gameplay image in " + ftype + " folder for benchmark:',benchmarkID
					if os.path.exists(l_path + file):
						if debug == 1:
							print '7:T'
						rhexdigest = md5Checksum(debug,r_path + file)
						lhexdigest = md5Checksum(debug,l_path + file)
						sql = "SELECT id, benchmarkID, chksum FROM " + table + " WHERE filename=%s AND benchmarkID=%s"
						args = (file, benchmarkID)
						cursor.execute(sql, args)
						if cursor.rowcount == 0:
							if debug == 1:
								print '8:F'
							sql = "INSERT into " + table + "(benchmarkID,filename,chksum) VALUES(%s,%s,%s)"
							args = (benchmarkID, file, rhexdigest)
							cursor.execute(sql, args)
							con.commit()
							logstr = ftype + " file not previously recorded but present in local repo:  " + file + "  benchmarkID:  " + str(benchmarkID)
							logit(debug,[logfiles['actlog'],logfiles['errlog']],"get_files",logstr)
						else:
							if debug == 1:
								print '8:T'
							for (chksum) in cursor:
								chksum = chksum[2]
							if rhexdigest != chksum:
								if debug == 1:
									print '9:F'
								if not os.path.exists(l_path + "\\archive\\"):
									if debug == 1:
										print '12:F'
									os.makedirs(l_path + "\\archive\\")
								else:
									if debug == 1:
										print '12:T'
								basename, extension = os.path.splitext(file)
								archfile = l_path + 'archive\\' + basename + "_" + archstamp + extension
								shutil.move(l_path + file, archfile) 
								shutil.copy (r_path + file, l_path + file)
								logstr = "Remote " + ftype + " file chksum does not match recorded for benchmarkID: " + str(benchmarkID) + "  New file recorded.  "
								logit(debug,[logfiles['actlog'],logfiles['chglog']],"get_files",logstr)
								sql = "UPDATE " + table + " SET vis_verified=NULL, chksum=%s WHERE filename=%s AND benchmarkID=%s"
								args = (rhexdigest,file,benchmarkID)
								try:
									cursor.execute(sql, args)
									con.commit()
								except mdb.Error, e:
									print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
							else:
								if debug == 1:
									print '9:T'									
								if rhexdigest != lhexdigest:
									if debug == 1:
										print '13:F'
									if not os.path.exists(l_path + "\\archive\\"):
										if debug == 1:
											print '14:F'
										os.makedirs(l_path + "\\archive\\")
									else:
										if debug == 1:
											print '14:T'
									basename, extension = os.path.splitext(file)
									archfile = l_path + 'archive\\' + basename + "_" + archstamp + extension
									shutil.move(l_path + file, archfile) 
									shutil.copy (r_path + file, l_path + file)
									sql = "UPDATE " + table + " SET vis_verified=NULL WHERE filename=%s AND benchmarkID=%s"
									args = (file,benchmarkID)
									try:
										cursor.execute(sql, args)
										con.commit()
									except mdb.Error, e:
										print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
									logstr = "Remote " + ftype + " file chksum matches recorded chksum but not local file chksum for benchmarkdID:  " + str(benchmarkID) + "  Local file updated and old version archived as " + archfile
									logit(debug,[logfiles['actlog'],logfiles['chglog']],"get_files",logstr)
								else:
									if debug == 1:
										print '13:T'
										logstr = "Remote " + ftype + " file chksum matches recorded chksum and local file chksum for benchmarkdID:  " + str(benchmarkID) + '  No changes.'
										logit(debug,[logfiles['actlog']],"get_files",logstr)		
					else:
						if debug == 1:
							print '7:F'
						shutil.copy (r_path + file, l_path + file)
						lhexdigest = md5Checksum(debug,l_path + file)
						sql = "SELECT id, benchmarkID, chksum FROM " + table + " WHERE filename=%s AND benchmarkID=%s"
						args = (file, benchmarkID)
						cursor.execute(sql, args)
						if cursor.rowcount == 0:
							if debug == 1:
								print '10:T'
							sql = "INSERT into " + table + "(benchmarkID,filename,chksum) VALUES(%s,%s,%s)"
							args = (benchmarkID, file, lhexdigest)
							cursor.execute(sql, args)
							con.commit()
							logstr = "New " + ftype + " file recorded and saved in local repo:  " + file + "  benchmarkID:  " + str(benchmarkID)
							logit(debug,[logfiles['actlog'],logfiles['chglog']],"get_files",logstr)
						else:
							if debug == 1:
								print '10:F'
							for (chksum) in cursor:
								chksum = chksum[3]
							if lhexdigest != chksum:
								if debug == 1:
									print '11:F'
								sql = "UPDATE " + table + " SET vis_verified=NULL, chksum=%s WHERE filename=%s AND benchmarkID=%s"
								args = (lhexdigest,file,benchmarkID)
								try:
									cursor.execute(sql, args)
									con.commit()
								except mdb.Error, e:
									print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
								logstr = ftype + " file of same name recorded for benchmarkID but with different chksum.  Local file was not present.  BenchmarkID: " + str(benchmarkID) + "  filename:  " + file
								logit(debug,[logfiles['actlog'],logfiles['errlog']],"get_files",logstr)
							else:
								if debug == 1:
									print '11:T'
								logstr = ftype + " file was previously recorded but local copy deleted:  " + file + "  benchmarkID:  " + str(benchmarkID)
								logit(debug,[logfiles['actlog'],logfiles['errlog']],"get_files",logstr)
					n = n + 1
				else:
					if debug == 1:
						print '6:F'
#				n = n + 1
				if debug == 1:
					print 'num_files:',n
			if ftype == 'screenshot':
				sql = "UPDATE tblBenchmarks SET num_screenshots=%s WHERE benchmarkID=%s"
			elif ftype == 'config':
				sql = "UPDATE tblBenchmarks SET num_configs=%s WHERE benchmarkID=%s"
			args = (n, [benchmarkID])
			try:
				print 'sql:', sql
				print 'args:', args
				cursor.execute(sql, args)
				con.commit()
			except mdb.Error, e:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		else:
			if debug == 1:
				print '5:F'
			if ftype == 'screenshot':
				print 'ftype:', ftype
				sql = "UPDATE tblBenchmarks SET num_screenshots=0 WHERE benchmarkID=%s"
			elif ftype == 'config':
				print 'ftype:', ftype
				sql = "UPDATE tblBenchmarks SET num_configs=0 WHERE benchmarkID=%s"
			try:
				cursor.execute(sql, [benchmarkID])
				con.commit()
			except mdb.Error, e:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

def write_thumbnail(debug,logfiles,con,cursor,thumbnail,thmb_path,taskid,archstamp):
	if debug == 1:
		print 'be_functions: write_thumbnail'
	thmbname = str(taskid) + '.jpg'
	tmpname = 'tmp.jpg'
	if not os.path.exists(thmb_path):
		os.makedirs(thmb_path)
	LfileList=os.listdir(thmb_path)
	for Lfile in LfileList:
		if Lfile != thmbname and os.path.isfile(thmb_path + Lfile):
			print 'file not found in remote repository.  Archiving:', Lfile
			if not os.path.exists(thmb_path + "\\archive\\"):
				os.makedirs(thmb_path + "\\archive\\")
			basename, extension = os.path.splitext(Lfile)
			archfile = thmb_path + 'archive\\' + basename + "_" + archstamp + extension
			shutil.move(thmb_path + Lfile, archfile)
			logstr = "Orphaned file found in thumbnail directory and moved to archive:  " + archfile
			logit(debug,[logfiles['actlog']],"write_thumbnail",logstr)		
	if os.path.isfile(thmb_path + thmbname):
		fi = open(thmb_path + tmpname, 'wb')
		fi.write(thumbnail.decode('base64'))	
		fi.close()
		old_chksum = md5Checksum(debug,thmb_path + thmbname)
		chksum = md5Checksum(debug,thmb_path + tmpname)
		if old_chksum == chksum:
			os.remove(thmb_path + tmpname)
			logstr = "Existing thumbnail found with matching checksum.  No Change"
			logit(debug,[logfiles['actlog']],"write_thumbnail",logstr)
		else:
			if not os.path.exists(thmb_path + 'archive\\'):
				os.makedirs(thmb_path + 'archive\\')
			archfile = thmb_path + 'archive\\' + str(taskid) + "_" + archstamp + ".jpg"				
			shutil.move(thmb_path + thmbname, archfile)
			shutil.move(thmb_path + tmpname, thmb_path + thmbname)
			sql = "UPDATE tblTitles SET thmb_vis_verified=NULL, thmb_chksum=%s WHERE gameID=%s"
			args = (chksum,taskid)
			try:
				cursor.execute(sql, args)
				con.commit()
			except mdb.Error, e:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			logstr = "New thumbnail recorded:  " + thmbname  + "  Old thumbnail archived:  " + archfile
			logit(debug,[logfiles['actlog'],logfiles['chglog']],"write_thumbnail",logstr)	
	else:
		fi = open(thmb_path + thmbname, 'wb')
		fi.write(thumbnail.decode('base64'))
		fi.close()
		chksum = md5Checksum(debug,thmb_path + thmbname)
		sql = "UPDATE tblTitles SET thmb_vis_verified=NULL, thmb_chksum=%s WHERE gameID=%s"
		args = (chksum,taskid)
		try:
			cursor.execute(sql, args)
			con.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		logstr = "New thumbnail file recorded:  " + thmbname
		logit(debug,[logfiles['actlog'],logfiles['chglog']],"write_thumbnail",logstr)	
