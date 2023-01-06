import MySQLdb
import sys

print 'Create Backend Database'
print 'Choose environment:\n'
print '1) Development\n'
print '2) Test\n'
print '3) Production\n'

u_in = raw_input("Enter 1, 2 or 3 (or q to quit): ")
while u_in not in ['1','2','3','q']:
	print "Invalid Entry"
	u_in = raw_input("Enter 1, 2 or 3 (or q to quit): ")
if u_in == '1':
	sql = 'CREATE DATABASE iggebedbdev'	
elif u_in == '2':
	sql = 'CREATE DATABASE iggebedbtst'
elif u_in == '3':
	sql = 'CREATE DATABASE iggebedbprd'
elif u_in == 'q':
	print 'Operation canceled.  Exiting Program'
	sys.exit()
else:
	print 'Invalid entry.  Exiting program.'
	sys.exit()

db = MySQLdb.connect(host='localhost',user='root',passwd='_PW_')
cursor = db.cursor()
cursor.execute(sql)

print 'Hit return to exit'
raw_input()
