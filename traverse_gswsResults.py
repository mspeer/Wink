#	Command line arguments are available to bypass user prompt and to allow for automation front end.  Valid entries are n,c or q
#		corresponding to new run, continuation run and quit respectively.  This checks for the presence of completed.txt which lists
#		titles that have been completed and creates this file is it doesn't exist.

import os, sys, glob, re, shutil, hashlib
import MySQLdb as mdb
import pyodbc, base64
from io import BytesIO
from PIL import Image
import unicodedata
import datetime

from be_functions import md5Checksum
from be_functions import logit
from be_functions import initapp
from be_functions import get_benchmarkID
from be_functions import get_dashboard_data
from be_functions import get_gsws_games_list
from be_functions import get_titleID_iggeqadb
from be_functions import get_platform_list
from be_functions import get_platformID_iggeqadb
from be_functions import get_labId_iggeqadb
from be_functions import get_paths_iggeqadb
from be_functions import get_files
from be_functions import get_taskId_gsws
from be_functions import Logger

dtstart = datetime.datetime.now()
dtstamp =  str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
archstamp = str(datetime.datetime.now().strftime("%Y%m%d%H%M"))
debug = 1
init_data = initapp(debug,dtstamp,dtstart,archstamp)
l_path_base = init_data[0]
conbe = init_data[1]
completedfile = init_data[2]
excludefile = init_data[3]
logfiles = init_data[4]
cursorbe = conbe.cursor()	
logit(debug,[logfiles['errlog'],logfiles['chglog'],logfiles['actlog']],"traverse_gswsResults root","Begin run")
gswsgameList = get_gsws_games_list(debug,logfiles)						#	Games List
for gswsgame in gswsgameList:
	f = open(excludefile)
	lines = f.readlines()
	excludes = [str(e.strip()) for e in lines]
	c = open(completedfile)	
	comp = c.readlines()	
	completed = [str(d.strip()) for d in comp]
	f.close
	c.close
	if gswsgame.TaskName in excludes:
		print 'game excluded:',gswsgame.TaskName
	elif gswsgame.TaskName in completed:
		print 'game already completed:',gswsgame.TaskName
	else:
		#  Need to search gsws for gsws.TaskName and choose only the latest TaskId.  Then replace all gsws.TaskId's with this new taskId.
		print '\n'
		print '------------------------------------------------------------------------------------------'
		print '*************************','Processing game:',gswsgame.TaskName,'*************************'
		print '------------------------------------------------------------------------------------------'
		TaskId = get_taskId_gsws(debug,logfiles,gswsgame.TaskName)
		titleId = get_titleID_iggeqadb(debug,logfiles,conbe,cursorbe,TaskId,gswsgame.TaskName)		#titleID
		print 'Determined taskId:',TaskId,'corresponding titleId:',titleId
		platformList = get_platform_list(debug,logfiles,TaskId)
		for platformdata in platformList:
			platform = platformdata.RecommendedRootPath.split('\\')[len(platformdata.RecommendedRootPath.split('\\'))-3]
			labName = platformdata.RecommendedRootPath.split('\\')[2].split('.')[0]
			labId = get_labId_iggeqadb(debug,logfiles,conbe,cursorbe,labName)
			pdata = get_platformID_iggeqadb(debug,logfiles,conbe,cursorbe,platform,platformdata.BucketId,platformdata.BucketName)		#platformID
			platformId = pdata[0]
			bucketed = pdata[1]
			bucketId = pdata[2]
			bucketName = pdata[3]
			benchmarkId = get_benchmarkID(debug,logfiles,conbe,cursorbe,labId,titleId,TaskId,platformId)		#benchmarkID
			print '\n'
			print '---------------------------------------------------------------------------------------------'
			print 'platform:',platform,'platformId:',platformId,'bucketed:',bucketed,'bucketId:',bucketId,'bucketName:',bucketName
			print '---------------------------------------------------------------------------------------------'
			paths = get_paths_iggeqadb(debug,logfiles,conbe,cursorbe,labId)
			r_path_base = paths[0]
			gname = get_dashboard_data(debug,logfiles,conbe,cursorbe,TaskId,benchmarkId,platformId,bucketed,archstamp,l_path_base,titleId)				#Get dashboard data for gameID(taskID)
			r_path = platformdata.RecommendedRootPath
			l_path = l_path_base + '\\' + gname + '\\RTM\\' + str(TaskId) + '\\benchmarks\\' + platform + '\\Recommended\\'
			ftype = 'screenshot'
			get_files(debug,logfiles,conbe,cursorbe,platformdata.RecommendedRootPath,l_path,ftype,benchmarkId,archstamp)
			r_path = r_path + 'GameSettingFiles\\'
			l_path= l_path + 'GameSettingFiles\\'
			ftype = 'config'
			get_files(debug,logfiles,conbe,cursorbe,r_path,l_path,ftype,benchmarkId,archstamp)
		c = open( completedfile, 'a' )
		c.write(gswsgame.TaskName + '\n')
		c.close
logit(debug,[logfiles['errlog'],logfiles['chglog'],logfiles['actlog']],"traverse_gswsResults root","End run")
dtend = datetime.datetime.now()
dtime = dtend - dtstart
print 'End run:',str(dtend)
print 'Execution time:',str(dtime)
print '\n'
print 'Hit return to exit'
raw_input()	#This is to hold the window open after the script completes
