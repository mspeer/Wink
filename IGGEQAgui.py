<BU>import wx
import os
import MySQLdb as mdb
import wx.grid as gridlib
import time
import shutil
from wx.lib.pubsub import pub
import time

class ssDetailFrame(wx.Frame):
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, None, title="Screen Shot Detail View", size=(1280,840))
#		self.scroll = wx.ScrolledWindow(self, -1)
		self.createWidgets()
		pub.subscribe(self.ssDetailListener, "ssdetailpanelListener")

	def createWidgets(self):
		self.panel = wx.Panel(self)
		img = wx.EmptyImage(460,215)
		self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
										 wx.BitmapFromImage(img))
 
		self.gnameLbl = wx.StaticText(self.panel, label='Name:')
		self.gnameTxt = wx.TextCtrl(self.panel, size=(200,-1), style=wx.TE_READONLY)
		self.taskIDLbl = wx.StaticText(self.panel, label='TaskID:')
		self.taskIDTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.ssIDLbl = wx.StaticText(self.panel, label='ssID:')
		self.ssIDTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.envLbl = wx.StaticText(self.panel, label='Env:')
		self.envTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.verifLbl = wx.StaticText(self.panel,label='')
		self.imgWLbl = wx.StaticText(self.panel, label='Width (460px):')
		self.imgWTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.imgHLbl = wx.StaticText(self.panel, label='Height (215px):')
		self.imgHTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.bucketLbl = wx.StaticText(self.panel, label='Bucket:')
		self.bucketTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.platformLbl = wx.StaticText(self.panel, label='Test Platform:')
		self.platformTxt = wx.TextCtrl(self.panel, size=(120,-1), style=wx.TE_READONLY)
		self.pathLbl = wx.StaticText(self.panel, label='Local Path:')
		self.pathTxt = wx.TextCtrl(self.panel, size=(920,-1), style=wx.TE_READONLY)
		self.approveBtn = wx.Button(self.panel, label='Approve')
		self.approveBtn.Bind(wx.EVT_BUTTON, self.onApprove)
		self.rejectBtn = wx.Button(self.panel, label='Reject')
		self.rejectBtn.Bind(wx.EVT_BUTTON, self.onReject)
		self.cancelBtn = wx.Button(self.panel, label='Cancel')
		self.cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel)
		self.addCommentBtn = wx.Button(self.panel, label="Add Comment")
		self.addCommentBtn.Bind(wx.EVT_BUTTON, self.onAddComment)
		self.cancelCommentBtn = wx.Button(self.panel, label="Cancel Comment")
		self.cancelCommentBtn.Bind(wx.EVT_BUTTON, self.onCancelComment)
		self.cancelCommentBtn.Hide()
		self.commentLbl = wx.StaticText(self.panel, label='Comments:')
		self.commentTxt = wx.TextCtrl(self.panel, size=(540,250), style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.commentTxt.SetBackgroundColour((190,190,190))


		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.head1Sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.head2Sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.head3Sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.head4Sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.imgSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.cntrlSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.commentSizer = wx.BoxSizer(wx.VERTICAL)
		self.footerSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.comboSizer = wx.BoxSizer(wx.HORIZONTAL)


		self.head1Sizer.Add(self.gnameLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.gnameTxt, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.taskIDLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.taskIDTxt, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.ssIDLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.ssIDTxt, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.envLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.envTxt, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.verifLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.imgWLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.imgWTxt, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.imgHLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.imgHTxt, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.bucketLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.bucketTxt, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.platformLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.platformTxt, 0, wx.ALL, 5)


		self.imgSizer.Add(self.imageCtrl, 0, wx.ALL, 5)

		self.footerSizer.Add(self.pathLbl, 0, wx.ALL, 5)
		self.footerSizer.Add(self.pathTxt, 0, wx.ALL, 5)
		
		self.cntrlSizer.Add(self.approveBtn, 0, wx.ALL, 5)
		self.cntrlSizer.Add(self.rejectBtn, 0, wx.ALL, 5)
		self.cntrlSizer.Add(self.cancelBtn, 0, wx.ALL, 5)
		self.cntrlSizer.Add(self.addCommentBtn, 0, wx.ALL, 5)
		self.cntrlSizer.Add(self.cancelCommentBtn, 0, wx.ALL, 5)
 #       self.cntrlSizer.Add(browseBtn, 0, wx.ALL, 5)

 #		self.comboSizer.Add(self.footerSizer, 0, wx.ALL, 5)
 #		self.comboSizer.Add(self.cntrlSizer, 0, wx.ALL, 5)

		self.commentSizer.Add(self.commentLbl, 0, wx.ALL, 5)
		self.commentSizer.Add(self.commentTxt, 0, wx.ALL, 5)

		self.mainSizer.Add(self.head1Sizer, 0, wx.ALL, 5)
		self.mainSizer.Add(self.head2Sizer, 0, wx.ALL, 5)
		self.mainSizer.Add(self.head3Sizer, 0, wx.ALL, 5)
		self.mainSizer.Add(self.head4Sizer, 0, wx.ALL, 5)
		self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
						   0, wx.ALL|wx.EXPAND, 5)
		self.mainSizer.Add(self.imgSizer, 0, wx.ALL, 5)   
		self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
						   0, wx.ALL|wx.EXPAND, 5)
#		self.mainSizer.Add(self.comboSizer, 0, wx.ALL, 5)
		self.mainSizer.Add(self.footerSizer, 0, wx.ALL, 5)
		self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
						   0, wx.ALL|wx.EXPAND, 5)
		self.mainSizer.Add(self.cntrlSizer, 0, wx.ALL, 5)
		self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
						   0, wx.ALL|wx.EXPAND, 5)        
		self.mainSizer.Add(self.commentSizer, 0, wx.ALL, 5)
		self.panel.SetSizer(self.mainSizer)
#        self.mainSizer.Fit(self.frame)
 
		self.panel.Layout()

	def onApprove(self, event):
		sql = 'UPDATE tblscreenshots SET vis_verified = 1 WHERE ssID=%s'
		args = (self.ssid)
		try:
			self.cursor.execute(sql, [args])
			self.conbe.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		self.onClosessDetailFrame()

	def onReject(self, event):
		sql = 'UPDATE tblscreenshots SET vis_verified = 0 WHERE ssID=%s'
		args = (self.ssid)
		try:
			self.cursor.execute(sql, [args])
			self.conbe.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		self.onClosessDetailFrame()

	def onCancel(self, event):
		self.onClosessDetailFrame()

	def onAddComment(self, event):
		label = self.addCommentBtn.GetLabel()
		if label == 'Add Comment':
			self.addCommentBtn.SetLabel('Commit Comment')
			self.commentTxt.SetBackgroundColour((255,255,255))
			self.commentTxt.SetEditable(True)
			self.cancelCommentBtn.Show()
			if self.commentTxt.GetValue():
				self.commentTxt.AppendText('\n-------------------------\n') 
			self.panel.Layout()

		elif label == 'Commit Comment':
			self.addCommentBtn.SetLabel('Add Comment')
			self.commentTxt.SetEditable(False)
			self.commentTxt.SetBackgroundColour((190,190,190))
			self.cancelCommentBtn.Hide()
			comment = self.commentTxt.GetValue()
			for ch in ['\n-------------------------\n']:
				if ch in comment:
					comment = comment.replace(ch, '|')
			sql = 'UPDATE tblscreenshots SET comment = %s WHERE ssID=%s'
			args = (comment,[self.ssid])
			try:
				self.cursor.execute(sql, args)
				self.conbe.commit()
			except mdb.Error, e:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			sql = 'SELECT DISTINCT tblscreenshots.comment FROM tblscreenshots \
				WHERE tblscreenshots.ssID=%s \
				ORDER by tblscreenshots.ssID DESC'   	
			args = ([self.ssid]) 
			self.cursor.execute(sql,args)
			row = self.cursor.fetchone()
			comment = row[0]
			for ch in ['|']:
				if ch in comment:
					comment = comment.replace(ch, '\n-------------------------\n')
			self.commentTxt.SetValue(comment)
		self.panel.Refresh()

	def onCancelComment(self, event):
		self.addCommentBtn.SetLabel('Add Comment')
		self.commentTxt.SetEditable(False)
		self.commentTxt.SetBackgroundColour((190,190,190))
		self.cancelCommentBtn.Hide()
		sql = 'SELECT DISTINCT tblscreenshots.comment FROM tblscreenshots \
				WHERE tblscreenshots.ssID=%s \
				ORDER by tblscreenshots.ssID DESC'
		args = ([self.ssid]) 
		self.cursor.execute(sql,args)
		row = self.cursor.fetchone()
		comment = row[0]
		for ch in ['|']:
			if ch in comment:
				comment = comment.replace(ch, '\n-------------------------\n')
		self.commentTxt.SetValue(comment)
		self.panel.Refresh()

	def renderImage(self):
		filepath = self.pathTxt.GetValue()
		img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
		W = img.GetWidth()
		H = img.GetHeight()
		self.imgHTxt.SetValue(str(H))
		self.imgWTxt.SetValue(str(W))
		self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
		if W < 1280:
			W = 1280
		self.SetSize((W, H + 600))
		self.scroll = wx.ScrolledWindow(self, -1)	
		self.panel.Refresh()

	def onClosessDetailFrame(self):
		"""
		Closes secondary frame
	   """
		msg = self.ssid
		print 'self.ssid:',self.ssid
		self.Hide()
		frame = ssGridFrame()
		frame.Show()
		pub.sendMessage("ssgridpanelListener", message=self.env, arg2=self.bucket)
		self.Destroy()    

	def ssDetailListener(self, message, arg2=None, arg3=None):
		print "ssDetailFrame: Received the following message: " + message
		if arg2:
			print "ssDetailFrame: Received another arguments: " + str(arg2)
		print 'ssDetailFrame - message:', message
		print 'ssDetailFrame - arg2:', arg2
		print 'ssDetailFrame - arg3:', arg3
		self.env = message
		self.ssid = arg2
		self.bucket = arg3
		print 'env:',self.env, 'ssid:',self.ssid
		if self.env == 'Dev':
			print 'Development environment specified'
			self.conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
		elif self.env == 'Test':
			print 'Test environment specified'
			self.conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbtst')
		elif self.env == 'Prod':
			print 'Production environment specified'
			self.conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbprd')
		else:
			print 'Error:  environment not defined.  Setting to dev.'
			self.conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
		self.cursor = self.conbe.cursor()
		sql = 'SELECT DISTINCT name, tblbenchmarks.gameID, tblbenchmarks.bucketid, description, ssFilename, tblscreenshots.vis_verified, tblscreenshots.comment from tblscreenshots \
		join tblbenchmarks on tblscreenshots.benchmarkID = tblbenchmarks.benchmarkID \
		join tbltitles on tblbenchmarks.titleID = tbltitles.titleID \
		join tblplatforms on tblbenchmarks.platformID = tblplatforms.platformID \
		WHERE tblscreenshots.ssid = %s'
		args = ([self.ssid]) 
		print 'sql:',sql
		print 'ssid:',self.ssid
		self.cursor.execute(sql,args)
		print 'rowcount:', self.cursor.rowcount
		row = self.cursor.fetchone()
		gname = row[0]
		taskid = row[1]
		bucketid = row[2]
		platform = row[3]
		ssfilename = row[4]
		vis_verified = row[5]
		comment = row[6]
		if gname.find(':') or gname.find('/'):
			for ch in [':','/']:
				if ch in gname:
					gname = gname.replace(ch,"")
		sspath = 'D:\\Projects\\IGGE\\repo\\BERepo\\' + self.env + '\\' + gname + '\\RTM\\' + str(taskid) + '\\benchmarks\\' + platform + '\\Recommended\\'+ ssfilename
		if gname:
			self.gnameTxt.SetValue(gname)
			self.gnameTxt.SetBackgroundColour((0,255,0))
		else:
			self.gnameTxt.SetValue('Missing Value')
			self.gnameTxt.SetBackgroundColour((255,0,0))
		if taskid:
			self.taskIDTxt.SetValue(str(taskid))
			self.taskIDTxt.SetBackgroundColour((0,255,0))
		else:
			self.taskIDTxt.SetValue('Missing Value')
			self.taskIDTxt.SetBackgroundColour((255,0,0))
		if self.ssid:
			self.ssIDTxt.SetValue(str(self.ssid))
			self.ssIDTxt.SetBackgroundColour((0,255,0))
		else:
			self.ssIDTxt.SetValue('Missing Value')
			self.ssIDTxt.SetBackgroundColour((255,0,0))
		self.envTxt.SetValue(self.env)
		if vis_verified == 0:
			self.verifLbl.SetLabel('Rejected')
			self.verifLbl.SetBackgroundColour((255,0,0))
		elif vis_verified == 1:
			self.verifLbl.SetLabel('Accepted')
			self.verifLbl.SetBackgroundColour((0,255,0))
		else:
			self.verifLbl.SetLabel('New')
			self.verifLbl.SetBackgroundColour((255,255,0))
		if bucketid:
			self.bucketTxt.SetValue(str(bucketid))
			self.bucketTxt.SetBackgroundColour((0,255,0))
		else:
			self.bucketTxt.SetValue('Mising Value')
			self.bucketTxt.SetBackgroundColour((255,255,0))
		if platform:
			self.platformTxt.SetValue(platform)
			self.platformTxt.SetBackgroundColour((0,255,0))
		else:
			self.platformTxt.SetValue('Mising Value')
			self.platformTxt.SetBackgroundColour((255,255,0))
		if sspath:    
			self.pathTxt.SetValue(sspath)
			self.pathTxt.SetBackgroundColour((0,255,0))
		else:
			self.pathTxt.SetValue('Missing Path')
			self.pathTxt.SetBackgroundColour((255,0,0))
		if comment:
			for ch in ['|']:
				if ch in comment:
					comment = comment.replace(ch, '\n-------------------------\n')
			self.commentTxt.SetValue(comment)
		self.renderImage()


class ssGridFrame(wx.Frame):
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, None, title="Unvalidated Screen Shots Grid View", size=(1480,1280))
		pub.subscribe(self.ssGridListener, "ssgridpanelListener")

	def OnRightClick(self, event):
		x, y = self.myGrid.CalcUnscrolledPosition(event.GetX(), event.GetY())
		row, col = self.myGrid.XYToCell(x, y)
		taskid = self.ssmap[str(row)]
		print "taskid:", taskid
		print 'env:', self.env
		self.Hide() 
		frame = ssDetailFrame()
		frame.Show()
		pub.sendMessage("ssdetailpanelListener", message=self.env, arg2=taskid, arg3=self.bucket)
		self.Destroy()
		

	def ssGridListener(self, message, arg2=None):
		print 'Entered into ssGridListener'
		print "thmbGridFrame: Received the following message: " + message
		if arg2:
			print "thmbGridFrame: Received another arguments: " + str(arg2)

		panel = wx.Panel(self)
		self.env = message
		self.bucket = arg2
		if self.env == 'Dev':
			print 'Development environment specified'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
		elif self.env == 'Test':
			print 'Test environment specified'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbtst')
		elif self.env == 'Prod':
			print 'Production environment specified'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbprd')
		else:
			print 'Error:  environment not defined.  Setting to dev.'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
		cursor = conbe.cursor()
		if self.bucket == 'All':
			print 'All buckets'
			sql = 'SELECT DISTINCT name, tblbenchmarks.gameID, tblbenchmarks.bucketid, description, ssFilename, tblscreenshots.ssID from tblscreenshots \
			join tblbenchmarks on tblscreenshots.benchmarkID = tblbenchmarks.benchmarkID \
			join tbltitles on tblbenchmarks.titleID = tbltitles.titleID \
			join tblplatforms on tblbenchmarks.platformID = tblplatforms.platformID \
			WHERE tblscreenshots.vis_verified IS NULL \
			order by name asc, bucketid asc, ssFilename asc'
			cursor.execute(sql)
		else:
			print 'bucket:', self.bucket
			sql = 'SELECT DISTINCT name, tblbenchmarks.gameID, tblbenchmarks.bucketid, description, ssFilename, tblscreenshots.ssID from tblscreenshots \
			join tblbenchmarks on tblscreenshots.benchmarkID = tblbenchmarks.benchmarkID \
			join tbltitles on tblbenchmarks.titleID = tbltitles.titleID \
			join tblplatforms on tblbenchmarks.platformID = tblplatforms.platformID \
			WHERE tblbenchmarks.bucketid = %s AND tblscreenshots.vis_verified IS NULL\
			order by name asc, bucketid asc, ssFilename asc'
			cursor.execute(sql, self.bucket)
		numcols = 6
		numrows = cursor.rowcount
		myGrid = gridlib.Grid(panel)
		self.myGrid = myGrid
		self.myGrid.CreateGrid(numrows, numcols)
		rows = cursor.fetchall()        
		currow = 0
		self.ssmap = {}
		for row in rows:
			self.taskid = str(row[1])
			gname = row[0]
			taskid = row[1]
			bucketid = row[2]
			platform = row[3]
			ssFilename = row[4]
			ssid = row[5]
			if gname.find(':') or gname.find('/'):
				for ch in [':','/']:
					if ch in gname:
						gname = gname.replace(ch,"")
			sspath = 'D:\\Projects\\IGGE\\repo\\BERepo\\' + self.env + '\\' + gname + '\\RTM\\' + str(taskid) + '\\benchmarks\\' + platform + '\\Recommended\\'
#			img = wx.Bitmap(sspath+(ssFilename), wx.BITMAP_TYPE_ANY)
			img = wx.Image(sspath+ssFilename, wx.BITMAP_TYPE_ANY)
			self.W = img.GetWidth()
			self.H = img.GetHeight()
			self.AR = self.W/(self.H * 1.0)
			self.NH = 300
			self.NW = self.NH * self.AR
			img = img.Scale(self.NW,self.NH)
			imageRenderer = MyImageRenderer(wx.BitmapFromImage(img))
			self.myGrid.SetCellValue(currow, 0, gname)
			self.myGrid.SetCellValue(currow, 1, taskid)
			self.myGrid.SetCellValue(currow, 2, bucketid)
			self.myGrid.SetCellValue(currow, 3, platform)
			self.myGrid.SetCellValue(currow, 4, ssFilename)
			self.myGrid.SetCellRenderer(currow,5,imageRenderer)
			self.myGrid.SetColSize(5,img.GetWidth()+2)
			self.myGrid.SetRowSize(currow,img.GetHeight()+2)
			self.ssmap[str(currow)] = ssid
			currow = currow + 1

		self.myGrid.GetGridWindow().Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(myGrid)
		panel.SetSizer(sizer)
		self.Refresh()
		self.myGrid.ForceRefresh()

class thmbDetailFrame(wx.Frame):
	""""""
	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
#        self.frame = wx.Frame(None, title='Thumbnail Detail View')
		wx.Frame.__init__(self, None, title="Thumbnail Detail View", size=(620,840))
#        self.panel = wx.Panel(self.frame)
		self.createWidgets()
		pub.subscribe(self.thmbDetailListener, "detailpanelListener")
#        self.frame.Show()


	def createWidgets(self):
		self.panel = wx.Panel(self)
		img = wx.EmptyImage(460,215)
		self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY, 
										 wx.BitmapFromImage(img))
 
		self.gnameLbl = wx.StaticText(self.panel, label='Name:')
		self.gnameTxt = wx.TextCtrl(self.panel, size=(200,-1), style=wx.TE_READONLY)
		self.taskIDLbl = wx.StaticText(self.panel, label='TaskID:')
		self.taskIDTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.envLbl = wx.StaticText(self.panel, label='Env:')
		self.envTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.verifLbl = wx.StaticText(self.panel,label='')
		self.fdateLbl = wx.StaticText(self.panel, label='Finished Date:')
		self.fdateTxt = wx.TextCtrl(self.panel, size=(160,-1), style=wx.TE_READONLY)
		self.rdateLbl = wx.StaticText(self.panel, label='Release Date:')
		self.rdateTxt = wx.TextCtrl(self.panel, size=(160,-1), style=wx.TE_READONLY)
		self.imgWLbl = wx.StaticText(self.panel, label='Width (460px):')
		self.imgWTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.imgHLbl = wx.StaticText(self.panel, label='Height (215px):')
		self.imgHTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.imgAspectLbl = wx.StaticText(self.panel, label='Aspect Ratio W/H (2.14):')
		self.imgAspectTxt = wx.TextCtrl(self.panel, size=(40,-1), style=wx.TE_READONLY)
		self.pathLbl = wx.StaticText(self.panel, label='Local Path:')
		self.pathTxt = wx.TextCtrl(self.panel, size=(540,-1), style=wx.TE_READONLY)
 #       browseBtn = wx.Button(self.panel, label='Browse')
 #       browseBtn.Bind(wx.EVT_BUTTON, self.onBrowse)
		self.approveBtn = wx.Button(self.panel, label='Approve')
		self.approveBtn.Bind(wx.EVT_BUTTON, self.onApprove)
		self.rejectBtn = wx.Button(self.panel, label='Reject')
		self.rejectBtn.Bind(wx.EVT_BUTTON, self.onReject)
		self.cancelBtn = wx.Button(self.panel, label='Cancel')
		self.cancelBtn.Bind(wx.EVT_BUTTON, self.onCancel)
		self.addCommentBtn = wx.Button(self.panel, label="Add Comment")
		self.addCommentBtn.Bind(wx.EVT_BUTTON, self.onAddComment)
		self.cancelCommentBtn = wx.Button(self.panel, label="Cancel Comment")
		self.cancelCommentBtn.Bind(wx.EVT_BUTTON, self.onCancelComment)
		self.cancelCommentBtn.Hide()
		self.commentLbl = wx.StaticText(self.panel, label='Comments:')
		self.commentTxt = wx.TextCtrl(self.panel, size=(540,250), style=wx.TE_MULTILINE|wx.TE_READONLY)
		self.commentTxt.SetBackgroundColour((190,190,190))


		self.mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.head1Sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.head2Sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.head3Sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.head4Sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.imgSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.cntrlSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.commentSizer = wx.BoxSizer(wx.VERTICAL)
		self.footerSizer = wx.BoxSizer(wx.VERTICAL)


		self.head1Sizer.Add(self.gnameLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.gnameTxt, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.taskIDLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.taskIDTxt, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.envLbl, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.envTxt, 0, wx.ALL, 5)
		self.head1Sizer.Add(self.verifLbl, 0, wx.ALL, 5)
		self.head2Sizer.Add(self.fdateLbl, 0, wx.ALL, 5)
		self.head2Sizer.Add(self.fdateTxt, 0, wx.ALL, 5)
		self.head2Sizer.Add(self.rdateLbl, 0, wx.ALL, 5)
		self.head2Sizer.Add(self.rdateTxt, 0, wx.ALL, 5)
		self.head3Sizer.Add(self.imgWLbl, 0, wx.ALL, 5)
		self.head3Sizer.Add(self.imgWTxt, 0, wx.ALL, 5)
		self.head3Sizer.Add(self.imgHLbl, 0, wx.ALL, 5)
		self.head3Sizer.Add(self.imgHTxt, 0, wx.ALL, 5)
		self.head3Sizer.Add(self.imgAspectLbl, 0, wx.ALL, 5)
		self.head3Sizer.Add(self.imgAspectTxt, 0, wx.ALL, 5)

		self.imgSizer.Add(self.imageCtrl, 0, wx.ALL, 5)

		self.footerSizer.Add(self.pathLbl, 0, wx.ALL, 5)
		self.footerSizer.Add(self.pathTxt, 0, wx.ALL, 5)
		
		self.cntrlSizer.Add(self.approveBtn, 0, wx.ALL, 5)
		self.cntrlSizer.Add(self.rejectBtn, 0, wx.ALL, 5)
		self.cntrlSizer.Add(self.cancelBtn, 0, wx.ALL, 5)
		self.cntrlSizer.Add(self.addCommentBtn, 0, wx.ALL, 5)
		self.cntrlSizer.Add(self.cancelCommentBtn, 0, wx.ALL, 5)
 #       self.cntrlSizer.Add(browseBtn, 0, wx.ALL, 5)

		self.commentSizer.Add(self.commentLbl, 0, wx.ALL, 5)
		self.commentSizer.Add(self.commentTxt, 0, wx.ALL, 5)

		self.mainSizer.Add(self.head1Sizer, 0, wx.ALL, 5)
		self.mainSizer.Add(self.head2Sizer, 0, wx.ALL, 5)
		self.mainSizer.Add(self.head3Sizer, 0, wx.ALL, 5)
		self.mainSizer.Add(self.head4Sizer, 0, wx.ALL, 5)
		self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
						   0, wx.ALL|wx.EXPAND, 5)
		self.mainSizer.Add(self.imgSizer, 0, wx.ALL, 5)   
		self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
						   0, wx.ALL|wx.EXPAND, 5)
		self.mainSizer.Add(self.footerSizer, 0, wx.ALL, 5)
		self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
						   0, wx.ALL|wx.EXPAND, 5)
		self.mainSizer.Add(self.cntrlSizer, 0, wx.ALL, 5)
		self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY),
						   0, wx.ALL|wx.EXPAND, 5)        
		self.mainSizer.Add(self.commentSizer, 0, wx.ALL, 5)
		self.panel.SetSizer(self.mainSizer)
#        self.mainSizer.Fit(self.frame)
 
		self.panel.Layout()

		   #----------------------------------------------------------------------
	def thmbDetailListener(self, message, arg2=None):
		"""
		Listener function
		"""
		print "thmbDetailFrame: Received the following message: " + message
		if arg2:
			print "thmbDetailFrame: Received another arguments: " + str(arg2)
		print 'thmbDetailFrame - message:', message
		print 'thmbDetailFrame - arg2:', arg2
		self.env = message
		self.taskid = arg2
		print self.env, self.taskid
		if self.env == 'Dev':
			print 'Development environment specified'
			self.conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
		elif self.env == 'Test':
			print 'Test environment specified'
			self.conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbtst')
		elif self.env == 'Prod':
			print 'Production environment specified'
			self.conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbprd')
		else:
			print 'Error:  environment not defined.  Setting to dev.'
			self.conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
		self.cursor = self.conbe.cursor()  
		sql = 'SELECT DISTINCT tbltitles.name, tbltitles.finisheddate, tbltitles.releasedate, tbltitles.rank, tbltitles.thmb_vis_verified, tbltitles.comment FROM tbltitles \
				WHERE tbltitles.gameID=%s \
				ORDER by tbltitles.titleID DESC'
		args = ([self.taskid]) 
		self.cursor.execute(sql,args)
		row = self.cursor.fetchone()
		gname = row[0]
		fdate = row[1]
		rdate = row[2]
		rank = row[3]
		vis_verified = row[4]
		comment = row[5]
		if gname.find(':') or gname.find('/'):
			for ch in [':','/']:
				if ch in gname:
					gname = gname.replace(ch,"")
		thmbpath = 'D:\\Projects\\IGGE\\repo\\BERepo\\' + self.env + '\\' + gname + '\\RTM\\' + str(self.taskid) + '\\thumbnail\\' + str(self.taskid) + '.jpg'

		if gname:
			self.gnameTxt.SetValue(gname)
			self.gnameTxt.SetBackgroundColour((0,255,0))
		else:
			self.gnameTxt.SetValue('Missing Value')
			self.gnameTxt.SetBackgroundColour((255,0,0))
		if self.taskid:
			self.taskIDTxt.SetValue(str(self.taskid))
			self.taskIDTxt.SetBackgroundColour((0,255,0))
		else:
			self.taskIDTxt.SetValue('Missing Value')
			self.taskIDTxt.SetBackgroundColour((255,0,0))
		self.envTxt.SetValue(self.env)
		if vis_verified == 0:
			self.verifLbl.SetLabel('Rejected')
			self.verifLbl.SetBackgroundColour((255,0,0))
		elif vis_verified == 1:
			self.verifLbl.SetLabel('Accepted')
			self.verifLbl.SetBackgroundColour((0,255,0))
		else:
			self.verifLbl.SetLabel('New')
			self.verifLbl.SetBackgroundColour((255,255,0))
		if fdate:
			self.fdateTxt.SetValue(fdate)
			self.fdateTxt.SetBackgroundColour((0,255,0))
		else:
			self.fdateTxt.SetValue('Mising Value')
			self.fdateTxt.SetBackgroundColour((255,255,0))
		if rdate:
			self.rdateTxt.SetValue(rdate)
			self.rdateTxt.SetBackgroundColour((0,255,0))
		else:
			self.rdateTxt.SetValue('Missing Value')
			self.rdateTxt.SetBackgroundColour((255,0,0))
		if thmbpath:    
			self.pathTxt.SetValue(thmbpath)
			self.pathTxt.SetBackgroundColour((0,255,0))
		else:
			self.pathTxt.SetValue('Missing Path')
			self.pathTxt.SetBackgroundColour((255,0,0))
		if comment:
			for ch in ['|']:
				if ch in comment:
					comment = comment.replace(ch, '\n-------------------------\n')
			self.commentTxt.SetValue(comment)
		self.renderImage()
 
	def onApprove(self, event):
		sql = 'UPDATE tbltitles SET thmb_vis_verified = 1 WHERE gameID=%s'
		args = (self.taskid)
		try:
			self.cursor.execute(sql, [args])
			self.conbe.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		self.onClosethmbDetailFrame()

	def onReject(self, event):
		sql = 'UPDATE tbltitles SET thmb_vis_verified = 0 WHERE gameID=%s'
		args = (self.taskid)
		try:
			self.cursor.execute(sql, [args])
			self.conbe.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		self.onClosethmbDetailFrame()

	def onCancel(self, event):
		self.onClosethmbDetailFrame()

	def onAddComment(self, event):
		label = self.addCommentBtn.GetLabel()
		if label == 'Add Comment':
			self.addCommentBtn.SetLabel('Commit Comment')
			self.commentTxt.SetBackgroundColour((255,255,255))
			self.commentTxt.SetEditable(True)
			self.cancelCommentBtn.Show()
			if self.commentTxt.GetValue():
				self.commentTxt.AppendText('\n-------------------------\n') 
			self.panel.Layout()

		elif label == 'Commit Comment':
			self.addCommentBtn.SetLabel('Add Comment')
			self.commentTxt.SetEditable(False)
			self.commentTxt.SetBackgroundColour((190,190,190))
			self.cancelCommentBtn.Hide()
			comment = self.commentTxt.GetValue()
			for ch in ['\n-------------------------\n']:
				if ch in comment:
					comment = comment.replace(ch, '|')
			sql = 'UPDATE tbltitles SET comment = %s WHERE gameID=%s'
			args = (comment,[self.taskid])
			try:
				self.cursor.execute(sql, args)
				self.conbe.commit()
			except mdb.Error, e:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
			sql = 'SELECT DISTINCT tbltitles.comment FROM tbltitles \
				WHERE tbltitles.gameID=%s \
				ORDER by tbltitles.titleID DESC'   	
			args = ([self.taskid]) 
			self.cursor.execute(sql,args)
			row = self.cursor.fetchone()
			comment = row[0]
			for ch in ['|']:
				if ch in comment:
					comment = comment.replace(ch, '\n-------------------------\n')
			self.commentTxt.SetValue(comment)
		self.panel.Refresh()

	def onCancelComment(self, event):
		self.addCommentBtn.SetLabel('Add Comment')
		self.commentTxt.SetEditable(False)
		self.commentTxt.SetBackgroundColour((190,190,190))
		self.cancelCommentBtn.Hide()
		sql = 'SELECT DISTINCT tbltitles.comment FROM tbltitles \
				WHERE tbltitles.gameID=%s \
				ORDER by tbltitles.titleID DESC'
		args = ([self.taskid]) 
		self.cursor.execute(sql,args)
		row = self.cursor.fetchone()
		comment = row[0]
		for ch in ['|']:
			if ch in comment:
				comment = comment.replace(ch, '\n-------------------------\n')
		self.commentTxt.SetValue(comment)
		self.panel.Refresh()

	def renderImage(self):
		filepath = self.pathTxt.GetValue()
		img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
		W = img.GetWidth()
		H = img.GetHeight()
		AR = W/float(H)
		AR = '%.2f'%round(AR,2)
		self.imgHTxt.SetValue(str(H))
		self.imgWTxt.SetValue(str(W))
		self.imgAspectTxt.SetValue(str(AR))
		if W == 460:
			self.imgWTxt.SetBackgroundColour((0,255,0))
		else:
			self.imgWTxt.SetBackgroundColour((255,255,0))
		if H == 215:
			self.imgHTxt.SetBackgroundColour((0,255,0))
		else:
			self.imgHTxt.SetBackgroundColour((255,255,0))
		if AR == float(2.14):
			self.imgAspectTxt.SetBackgroundColour((0,255,0))
		else:
			self.imgAspectTxt.SetBackgroundColour((255,255,0))
		self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
		self.panel.Refresh()      

	def onClosethmbDetailFrame(self):
		"""
		Closes secondary frame
	   """
#        frame = thmbGridFrame()
#        frame.Show()
 
#        msg = self.msgTxt.GetValue()
		msg = self.taskid
		print 'self.taskid:',self.taskid
		self.Hide()
		frame = thmbGridFrame()
		frame.Show()
		pub.sendMessage("gridpanelListener", message=self.env)
		self.Destroy()
		


class thmbGridFrame(wx.Frame):
	""""""
#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, None, title="Unvalidated Thumbnail Grid View", size=(1480,1280))
		pub.subscribe(self.thmbGridListener, "gridpanelListener")

	def OnRightClick(self, event):
		x, y = self.myGrid.CalcUnscrolledPosition(event.GetX(), event.GetY())
		row, col = self.myGrid.XYToCell(x, y)
		taskid = self.thmbmap[str(row) + "_" + str(col)]
		print "taskid:", taskid
		print 'env:', self.env
		self.Hide() 
		frame = thmbDetailFrame()
		frame.Show()
		pub.sendMessage("detailpanelListener", message=self.env, arg2=taskid)
		self.Destroy()
		

	def thmbGridListener(self, message, arg2=None):
		"""
		Listener function
		"""
		print 'Entered into thmbGridListener'
		print "thmbGridFrame: Received the following message: " + message
		if arg2:
			print "thmbGridFrame: Received another arguments: " + str(arg2)

		panel = wx.Panel(self)
		self.env = message
		if self.env == 'Dev':
			print 'Development environment specified'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
		elif self.env == 'Test':
			print 'Test environment specified'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbtst')
		elif self.env == 'Prod':
			print 'Production environment specified'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbprd')
		else:
			print 'Error:  environment not defined.  Setting to dev.'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
		cursor = conbe.cursor()  
		sql = 'SELECT DISTINCT tbltitles.name, tblbenchmarks.gameID FROM tbltitles \
				JOIN tblbenchmarks ON tbltitles.titleID = tblbenchmarks.titleID \
				WHERE tbltitles.thmb_vis_verified IS NULL \
				ORDER by tbltitles.name ASC'    
		cursor.execute(sql)
		numcols = 3
		numrows = cursor.rowcount / 3
		if cursor.rowcount%3 > 0:
			numrows = numrows + 1
		myGrid = gridlib.Grid(panel)
		self.myGrid = myGrid
		self.myGrid.CreateGrid(numrows, numcols)
		rows = cursor.fetchall()        
		currow = 0
		curcol = 0
		self.thmbmap = {}
		for row in rows:
			self.taskid = str(row[1])
			gname = row[0]
			if gname.find(':') or gname.find('/'):
				for ch in [':','/']:
					if ch in gname:
						gname = gname.replace(ch,"")
			thmbpath = 'D:\\Projects\\IGGE\\repo\\BERepo\\' + self.env + '\\' + gname + '\\RTM\\' + str(row[1]) + '\\thumbnail\\'
			img = wx.Bitmap(thmbpath+str(self.taskid)+'.jpg', wx.BITMAP_TYPE_JPEG)
			imageRenderer = MyImageRenderer(img)
			self.myGrid.SetCellRenderer(currow,curcol,imageRenderer)
			self.myGrid.SetColSize(curcol,img.GetWidth()+2)
			self.myGrid.SetRowSize(currow,img.GetHeight()+2)
			self.thmbmap[str(currow)+"_"+str(curcol)] = self.taskid
			curcol = curcol + 1
			if curcol > 2:
				curcol = 0
				currow = currow + 1
		self.myGrid.GetGridWindow().Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(myGrid)
		panel.SetSizer(sizer)
		self.Refresh()
		self.myGrid.ForceRefresh()
		print 'End of thmbGridListener'

class ValFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="Data Validation")
		
		self.InitValUI()
	
	def InitValUI(self):
		self.valpnl = wx.Panel(self)
		
		valtypes = ['ScreenShots','Thumbnails','Configuration Files','All']
		self.cbvaltype = wx.ComboBox(self.valpnl, pos=(30,30), choices=valtypes, style=wx.CB_READONLY)
		self.cbvaltype.Bind(wx.EVT_COMBOBOX, self.ValOnSelect)
		self.cbvaltype.Enable()
		self.valtypest = wx.StaticText(self.valpnl, label='', pos=(30, 80))

		envtypes = ['development','test','production']
		self.cbenvtype = wx.ComboBox(self.valpnl, pos=(180,30), choices=envtypes, style=wx.CB_READONLY)
		self.cbenvtype.Bind(wx.EVT_COMBOBOX, self.EnvOnSelect)
		self.cbenvtype.Disable()
		self.envst = wx.StaticText(self.valpnl, label='', pos=(180,80))
		
		buckets = []
		self.cbbuckets = wx.ComboBox(self.valpnl, pos=(320,30), choices=buckets, style=wx.CB_READONLY)
		self.cbbuckets.Bind(wx.EVT_COMBOBOX, self.BucketsOnSelect)
		self.cbbuckets.Disable()
		self.cbbuckets.Hide()
		self.bucketst = wx.StaticText(self.valpnl, label='', pos=(320,80))
		
		self.btnretrieve = wx.Button(self.valpnl, id=wx.ID_ANY, pos=(500, 30), label='Retrieve')
		self.btnretrieve.Bind(wx.EVT_BUTTON, self.OnRetrieve)
		self.btnretrieve.Disable()
				
		self.SetSize((640, 480))
		self.Centre()
	
	def ValOnSelect(self, e):
		typ = e.GetString()
		self.valtypest.SetLabel(typ)
		self.cbenvtype.Enable()
		typ = self.cbvaltype.GetValue()
		if typ=='Thumbnails':
			self.cbbuckets.Hide()
		else:
			self.cbbuckets.Show()
		
	def EnvOnSelect(self, e):
		env = e.GetString()
		self.envst.SetLabel(env)
		typ = self.cbvaltype.GetValue()
		if env=='development':
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')	
		elif env=='test':
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbtst')
		else:
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbprd')
		cursor = conbe.cursor()
		if typ=='ScreenShots':
			sql = 'SELECT DISTINCT tblbenchmarks.bucketid FROM tblbenchmarks \
				JOIN tblscreenshots ON tblbenchmarks.benchmarkID = tblscreenshots.benchmarkID \
				WHERE tblscreenshots.vis_verified IS NULL \
				ORDER by tblbenchmarks.bucketid ASC'
		elif typ=='Configuration Files':
			sql = 'SELECT DISTINCT tblbenchmarks.bucketid FROM tblbenchmarks \
				JOIN tblconfigs ON tblbenchmarks.benchmarkID = tblconfigs.benchmarkID \
				WHERE tblconfigs.vis_verified IS NULL \
				ORDER by tblbenchmarks.bucketid ASC'
		else:
			sql = 'SELECT DISTINCT tblbenchmarks.bucketid FROM tblbenchmarks \
				JOIN tblscreenshots ON tblbenchmarks.benchmarkID = tblscreenshots.benchmarkID  \
				JOIN tbltitles ON tblbenchmarks.titleID = tbltitles.titleID \
				JOIN tblconfigs ON tblbenchmarks.benchmarkID = tblconfigs.benchmarkID  \
				WHERE tblscreenshots.vis_verified=0 OR tbltitles.thmb_vis_verified=0 OR tblconfigs.vis_verified=0 \
				ORDER by tblbenchmarks.bucketid ASC'
		if typ!='Thumbnails':
			cursor.execute(sql)
			if cursor.rowcount == 0:
				print 'No records retrieved'
			else:
				buckets = []
				dataset = cursor.fetchall()
				for data in dataset:
					buckets.append(str(data[0]))
				self.cbbuckets.SetItems(buckets)
				self.cbbuckets.Append('All')
				self.cbbuckets.Enable()
		else:
			self.btnretrieve.Enable()
		
	def BucketsOnSelect(self, e):
		i = e.GetString()
		self.bucketst.SetLabel(i)
		self.btnretrieve.Enable()
	
	def OnRetrieve(self, e):
		env = self.cbenvtype.GetValue()
		typ = self.cbvaltype.GetValue()
		bucket = self.cbbuckets.GetValue()
		if typ!='Thumbnails':
			bucket = self.cbbuckets.GetValue()
		if env=='development':
			env = 'Dev'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')	
		elif env=='test':
			env = 'Test'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbtst')
		else:
			env = 'Prod'
			conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbprd')
		cursor = conbe.cursor()
		if typ=='ScreenShots':
			sql = 'SELECT DISTINCT tblbenchmarks.bucketid FROM tblbenchmarks \
				JOIN tblscreenshots ON tblbenchmarks.benchmarkID = tblscreenshots.benchmarkID \
				WHERE tblscreenshots.vis_verified=0 \
				ORDER by tblbenchmarks.bucketid ASC'
			frame = ssGridFrame()
			frame.Show()
			pub.sendMessage("ssgridpanelListener", message=env, arg2=bucket)
		elif typ=='Thumbnails':
			print 'env:',env
			frame = thmbGridFrame()
			frame.Show()
			pub.sendMessage("gridpanelListener", message=env)

#		elif typ=='Configuration Files':
#			sql = 'SELECT DISTINCT tblbenchmarks.bucketid FROM tblbenchmarks \
#				JOIN tblconfigs ON tblbenchmarks.benchmarkID = tblconfigs.benchmarkID \
#				WHERE tblconfigs.vis_verified=0 \
#				ORDER by tblbenchmarks.bucketid ASC'
#		else:
#			sql = 'SELECT DISTINCT tblbenchmarks.bucketid FROM tblbenchmarks \
#				JOIN tblscreenshots ON tblbenchmarks.benchmarkID = tblscreenshots.benchmarkID  \
#				JOIN tbltitles ON tblbenchmarks.titleID = tbltitles.titleID \
#				JOIN tblconfigs ON tblbenchmarks.benchmarkID = tblconfigs.benchmarkID  \
#				WHERE tblscreenshots.vis_verified=0 OR tbltitles.thmb_vis_verified=0 OR tblconfigs.vis_verified=0 \
#				ORDER by tblbenchmarks.bucketid ASC'

class MainFrame(wx.Frame):
	def __init__(self, *args, **kwargs):
		super(MainFrame, self).__init__(*args, **kwargs)
		
		self.InitUI()
		
	def InitUI(self):
	
		menubar = wx.MenuBar()
		
		dataMenu = wx.Menu()
		
		beMenu = wx.Menu()
		be_dev = wx.Menu()
		be_dev_n = wx.MenuItem(be_dev, wx.ID_ANY, 'New execution')
		be_dev.AppendItem(be_dev_n)
		be_dev_c = wx.MenuItem(be_dev, wx.ID_ANY, 'Continuation execution')
		be_dev.AppendItem(be_dev_c)
		beMenu.AppendMenu(wx.ID_ANY, 'Development Environment', be_dev)
		be_tst = wx.Menu()
		be_tst_n = wx.MenuItem(be_tst, wx.ID_ANY, 'New execution')
		be_tst.AppendItem(be_tst_n)
		be_tst_c = wx.MenuItem(be_tst, wx.ID_ANY, 'Continuation execution')
		be_tst.AppendItem(be_tst_c)
		beMenu.AppendMenu(wx.ID_ANY, 'Test Environment', be_tst)
		be_prd = wx.Menu()
		be_prd_n = wx.MenuItem(be_prd, wx.ID_ANY, 'New execution')
		be_prd.AppendItem(be_prd_n)
		be_prd_c = wx.MenuItem(be_prd, wx.ID_ANY, 'Continuation execution')
		be_prd.AppendItem(be_prd_c)
		beMenu.AppendMenu(wx.ID_ANY, 'Production Environment', be_prd)
		dataMenu.AppendMenu(wx.ID_ANY, 'Refresh Backend Data', beMenu)
		
		dataMenu.AppendSeparator()
		
		ssMenu = wx.Menu()
		ss_dev = wx.MenuItem(ssMenu, wx.ID_ANY, 'Development Environment')
		ssMenu.AppendItem(ss_dev)
		ss_tst = wx.MenuItem(ssMenu, wx.ID_ANY, 'Test Environment')
		ssMenu.AppendItem(ss_tst)
		ss_prd = wx.MenuItem(ssMenu, wx.ID_ANY, 'Production Environment')
		ssMenu.AppendItem(ss_prd)
		
		dataMenu.AppendMenu(wx.ID_ANY, 'Generate Snapshot', ssMenu)
		
		menubar.Append(dataMenu, 'Data')
		
		rptMenu = wx.Menu()
		rptMenu.Append(5, 'Readiness')
		
		menubar.Append(rptMenu, 'Reports')
		
		verMenu = wx.Menu()
		vermi = wx.MenuItem(verMenu, wx.ID_ANY, 'Vis Verify')
		verMenu.AppendItem(vermi)
		menubar.Append(verMenu, 'Verify')
		
		adminMenu = wx.Menu()
		dbtoolsMenu = wx.Menu()
		dbriMenu = wx.Menu()
		bedbriMenu = wx.Menu()
		bedbrienvMenu = wx.Menu()
		bedbrienvdev = wx.Menu()
		bedbrienvdevtblbenchmarks = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'tblBenchmarks')
		bedbrienvdev.AppendItem(bedbrienvdevtblbenchmarks)
		bedbrienvdevtblcomments = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'tblComments')
		bedbrienvdev.AppendItem(bedbrienvdevtblcomments)
		bedbrienvdevtblconfigs = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'tblConfigs')
		bedbrienvdev.AppendItem(bedbrienvdevtblconfigs)
		bedbrienvdevtbldeviceids = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'tbldeviceids')
		bedbrienvdev.AppendItem(bedbrienvdevtbldeviceids)
		bedbrienvdevtbllabs = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'tblLabs')
		bedbrienvdev.AppendItem(bedbrienvdevtbllabs)
		bedbrienvdevtbllogs = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'tblLogs')
		bedbrienvdev.AppendItem(bedbrienvdevtbllogs)
		bedbrienvdevtblplatforms = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'tblPlatforms')
		bedbrienvdev.AppendItem(bedbrienvdevtblplatforms)
		bedbrienvdevtblscreenshots = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'tblScreenShots')
		bedbrienvdev.AppendItem(bedbrienvdevtblscreenshots)
		bedbrienvdevtbltitles = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'tblTitles')
		bedbrienvdev.AppendItem(bedbrienvdevtbltitles)
		bedbrienvdevtbltoptitles = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'tblTOPTitles')
		bedbrienvdev.AppendItem(bedbrienvdevtbltoptitles)
		bedbrienvdevtblall = wx.MenuItem(bedbrienvdev, wx.ID_ANY, 'All Tables')
		bedbrienvdev.AppendItem(bedbrienvdevtblall)
		bedbrienvMenu.AppendMenu(wx.ID_ANY, 'Development', bedbrienvdev)		
		bedbrienvtst = wx.Menu()
		bedbrienvtsttblbenchmarks = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'tblBenchmarks')
		bedbrienvtst.AppendItem(bedbrienvtsttblbenchmarks)
		bedbrienvtsttblcomments = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'tblComments')
		bedbrienvtst.AppendItem(bedbrienvtsttblcomments)
		bedbrienvtsttblconfigs = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'tblConfigs')
		bedbrienvtst.AppendItem(bedbrienvtsttblconfigs)
		bedbrienvtsttbldeviceids = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'tbldeviceids')
		bedbrienvtst.AppendItem(bedbrienvtsttbldeviceids)
		bedbrienvtsttbllabs = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'tblLabs')
		bedbrienvtst.AppendItem(bedbrienvtsttbllabs)
		bedbrienvtsttbllogs = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'tblLogs')
		bedbrienvtst.AppendItem(bedbrienvtsttbllogs)
		bedbrienvtsttblplatforms = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'tblPlatforms')
		bedbrienvtst.AppendItem(bedbrienvtsttblplatforms)
		bedbrienvtsttblscreenshots = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'tblScreenShots')
		bedbrienvtst.AppendItem(bedbrienvtsttblscreenshots)
		bedbrienvtsttbltitles = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'tblTitles')
		bedbrienvtst.AppendItem(bedbrienvtsttbltitles)
		bedbrienvtsttbltoptitles = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'tblTOPTitles')
		bedbrienvtst.AppendItem(bedbrienvtsttbltoptitles)
		bedbrienvtsttblall = wx.MenuItem(bedbrienvtst, wx.ID_ANY, 'All Tables')
		bedbrienvtst.AppendItem(bedbrienvtsttblall)
		bedbrienvMenu.AppendMenu(wx.ID_ANY, 'Test', bedbrienvtst)		
		bedbrienvprd = wx.Menu()
		bedbrienvprdtblbenchmarks = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'tblBenchmarks')
		bedbrienvprd.AppendItem(bedbrienvprdtblbenchmarks)
		bedbrienvprdtblcomments = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'tblComments')
		bedbrienvprd.AppendItem(bedbrienvprdtblcomments)
		bedbrienvprdtblconfigs = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'tblConfigs')
		bedbrienvprd.AppendItem(bedbrienvprdtblconfigs)
		bedbrienvprdtbldeviceids = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'tbldeviceids')
		bedbrienvprd.AppendItem(bedbrienvprdtbldeviceids)
		bedbrienvprdtbllabs = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'tblLabs')
		bedbrienvprd.AppendItem(bedbrienvprdtbllabs)
		bedbrienvprdtbllogs = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'tblLogs')
		bedbrienvprd.AppendItem(bedbrienvprdtbllogs)
		bedbrienvprdtblplatforms = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'tblPlatforms')
		bedbrienvprd.AppendItem(bedbrienvprdtblplatforms)
		bedbrienvprdtblscreenshots = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'tblScreenShots')
		bedbrienvprd.AppendItem(bedbrienvprdtblscreenshots)
		bedbrienvprdtbltitles = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'tblTitles')
		bedbrienvprd.AppendItem(bedbrienvprdtbltitles)
		bedbrienvprdtbltoptitles = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'tblTOPTitles')
		bedbrienvprd.AppendItem(bedbrienvprdtbltoptitles)
		bedbrienvprdtblall = wx.MenuItem(bedbrienvprd, wx.ID_ANY, 'All Tables')
		bedbrienvprd.AppendItem(bedbrienvprdtblall)		
		bedbrienvMenu.AppendMenu(wx.ID_ANY, 'Production', bedbrienvprd)
		dbriMenu.AppendMenu(wx.ID_ANY, 'IGGEBEdb', bedbrienvMenu)
		ssdbMenu = wx.Menu()
		ssdbriMenu = wx.Menu()
		ssdbrienvMenu = wx.Menu()
		ssdbrienvdev = wx.Menu()
		ssdbrienvdevtblss = wx.MenuItem(ssdbrienvdev, wx.ID_ANY,'tblShapshots')
		ssdbrienvdev.AppendItem(ssdbrienvdevtblss)
		ssdbrienvdevtblssbenchmarks = wx.MenuItem(ssdbrienvdev, wx.ID_ANY,'tblSSBenchmarks')
		ssdbrienvdev.AppendItem(ssdbrienvdevtblssbenchmarks)
		ssdbrienvdevtblssconfigs = wx.MenuItem(ssdbrienvdev, wx.ID_ANY,'tblSSConfigs')
		ssdbrienvdev.AppendItem(ssdbrienvdevtblssconfigs)
		ssdbrienvdevtblssdeviceids = wx.MenuItem(ssdbrienvdev, wx.ID_ANY,'tblSSDeviceIds')
		ssdbrienvdev.AppendItem(ssdbrienvdevtblssdeviceids)
		ssdbrienvdevtblssscreenshots = wx.MenuItem(ssdbrienvdev, wx.ID_ANY,'tblSSScreenShots')
		ssdbrienvdev.AppendItem(ssdbrienvdevtblssscreenshots)
		ssdbrienvdevtblssthumbnails = wx.MenuItem(ssdbrienvdev, wx.ID_ANY,'tblSSThumbnails')
		ssdbrienvdev.AppendItem(ssdbrienvdevtblssthumbnails)
		ssdbrienvdevtblsstitles = wx.MenuItem(ssdbrienvdev, wx.ID_ANY,'tblSSTitles')
		ssdbrienvdev.AppendItem(ssdbrienvdevtblsstitles)
		ssdbrienvdevtblall = wx.MenuItem(ssdbrienvdev, wx.ID_ANY,'All Tables')
		ssdbrienvdev.AppendItem(ssdbrienvdevtblall)
		ssdbrienvMenu.AppendMenu(wx.ID_ANY, 'Development', ssdbrienvdev)
		ssdbrienvtst = wx.Menu()
		ssdbrienvtsttblss = wx.MenuItem(ssdbrienvtst, wx.ID_ANY,'tblShapshots')
		ssdbrienvtst.AppendItem(ssdbrienvtsttblss)
		ssdbrienvtsttblssbenchmarks = wx.MenuItem(ssdbrienvtst, wx.ID_ANY,'tblSSBenchmarks')
		ssdbrienvtst.AppendItem(ssdbrienvtsttblssbenchmarks)
		ssdbrienvtsttblssconfigs = wx.MenuItem(ssdbrienvtst, wx.ID_ANY,'tblSSConfigs')
		ssdbrienvtst.AppendItem(ssdbrienvtsttblssconfigs)
		ssdbrienvtsttblssdeviceids = wx.MenuItem(ssdbrienvtst, wx.ID_ANY,'tblSSDeviceIds')
		ssdbrienvtst.AppendItem(ssdbrienvtsttblssdeviceids)
		ssdbrienvtsttblssscreenshots = wx.MenuItem(ssdbrienvtst, wx.ID_ANY,'tblSSScreenShots')
		ssdbrienvtst.AppendItem(ssdbrienvtsttblssscreenshots)
		ssdbrienvtsttblssthumbnails = wx.MenuItem(ssdbrienvtst, wx.ID_ANY,'tblSSThumbnails')
		ssdbrienvtst.AppendItem(ssdbrienvtsttblssthumbnails)
		ssdbrienvtsttblsstitles = wx.MenuItem(ssdbrienvtst, wx.ID_ANY,'tblSSTitles')
		ssdbrienvtst.AppendItem(ssdbrienvtsttblsstitles)
		ssdbrienvtsttblall = wx.MenuItem(ssdbrienvtst, wx.ID_ANY,'All Tables')
		ssdbrienvtst.AppendItem(ssdbrienvtsttblall)
		ssdbrienvMenu.AppendMenu(wx.ID_ANY, 'Test', ssdbrienvtst)
		ssdbrienvprd = wx.Menu()
		ssdbrienvprdtblss = wx.MenuItem(ssdbrienvprd, wx.ID_ANY,'tblShapshots')
		ssdbrienvprd.AppendItem(ssdbrienvprdtblss)
		ssdbrienvprdtblssbenchmarks = wx.MenuItem(ssdbrienvprd, wx.ID_ANY,'tblSSBenchmarks')
		ssdbrienvprd.AppendItem(ssdbrienvprdtblssbenchmarks)
		ssdbrienvprdtblssconfigs = wx.MenuItem(ssdbrienvprd, wx.ID_ANY,'tblSSConfigs')
		ssdbrienvprd.AppendItem(ssdbrienvprdtblssconfigs)
		ssdbrienvprdtblssdeviceids = wx.MenuItem(ssdbrienvprd, wx.ID_ANY,'tblSSDeviceIds')
		ssdbrienvprd.AppendItem(ssdbrienvprdtblssdeviceids)
		ssdbrienvprdtblssscreenshots = wx.MenuItem(ssdbrienvprd, wx.ID_ANY,'tblSSScreenShots')
		ssdbrienvprd.AppendItem(ssdbrienvprdtblssscreenshots)
		ssdbrienvprdtblssthumbnails = wx.MenuItem(ssdbrienvprd, wx.ID_ANY,'tblSSThumbnails')
		ssdbrienvprd.AppendItem(ssdbrienvprdtblssthumbnails)
		ssdbrienvprdtblsstitles = wx.MenuItem(ssdbrienvprd, wx.ID_ANY,'tblSSTitles')
		ssdbrienvprd.AppendItem(ssdbrienvprdtblsstitles)
		ssdbrienvprdtblall = wx.MenuItem(ssdbrienvprd, wx.ID_ANY,'All Tables')
		ssdbrienvprd.AppendItem(ssdbrienvprdtblall)
		ssdbrienvMenu.AppendMenu(wx.ID_ANY, 'Production', ssdbrienvprd)						
		dbriMenu.AppendMenu(wx.ID_ANY, 'IGGESSdb', ssdbrienvMenu)
		dbtoolsMenu.AppendMenu(wx.ID_ANY, 'Re-initialize', dbriMenu)
		adminMenu.AppendMenu(wx.ID_ANY, 'Database Tools', dbtoolsMenu)
		repotoolsMenu = wx.Menu()
		reporiMenu = wx.Menu()
		repotoolsMenu.AppendMenu(wx.ID_ANY, 'Re-initialize', reporiMenu)
		reporiberepo = wx.Menu()
		reporiberepodev = wx.MenuItem(reporiberepo, wx.ID_ANY, 'Development')
		reporiberepo.AppendItem(reporiberepodev)
		reporiberepotst = wx.MenuItem(reporiberepo, wx.ID_ANY, 'Test')
		reporiberepo.AppendItem(reporiberepotst)
		reporiberepoprd = wx.MenuItem(reporiberepo, wx.ID_ANY, 'Production')
		reporiberepo.AppendItem(reporiberepoprd)		
		reporiMenu.AppendMenu(wx.ID_ANY, 'BERepository', reporiberepo)
		reporissrepo = wx.Menu()
		reporissrepodev = wx.MenuItem(reporissrepo, wx.ID_ANY, 'Development')
		reporissrepo.AppendItem(reporissrepodev)
		reporissrepotst = wx.MenuItem(reporissrepo, wx.ID_ANY, 'Test')
		reporissrepo.AppendItem(reporissrepotst)
		reporissrepoprd = wx.MenuItem(reporissrepo, wx.ID_ANY, 'Production')
		reporissrepo.AppendItem(reporissrepoprd)
		reporiMenu.AppendMenu(wx.ID_ANY, 'SSRepository', reporissrepo)
		adminMenu.AppendMenu(wx.ID_ANY, 'Local Repository Tools', repotoolsMenu)
		menubar.Append(adminMenu, 'Admin')
				
		qMenu = wx.Menu()
		qmi = wx.MenuItem(qMenu, wx.ID_ANY, 'Quit Application')
		qMenu.AppendItem(qmi)
		menubar.Append(qMenu, 'Quit')
		
		self.Bind(wx.EVT_MENU, self.VisVerify, vermi)
		self.Bind(wx.EVT_MENU, self.OnQuit, qmi)
		self.Bind(wx.EVT_MENU, self.BEDevN, be_dev_n)
		self.Bind(wx.EVT_MENU, self.BEDevC, be_dev_c)
		self.Bind(wx.EVT_MENU, self.BETstN, be_tst_n)
		self.Bind(wx.EVT_MENU, self.BETstC, be_tst_c)
		self.Bind(wx.EVT_MENU, self.BEPrdN, be_prd_n)
		self.Bind(wx.EVT_MENU, self.BEPrdC, be_prd_c)
		self.Bind(wx.EVT_MENU, self.SSDev, ss_dev)
		self.Bind(wx.EVT_MENU, self.SSTst, ss_tst)
		self.Bind(wx.EVT_MENU, self.SSPrd, ss_prd)
		

		
		
		self.Bind(wx.EVT_MENU, self.RiBEDEVBenchmarks, bedbrienvdevtblbenchmarks)
		self.Bind(wx.EVT_MENU, self.RiBEDEVComments, bedbrienvdevtblcomments)
		self.Bind(wx.EVT_MENU, self.RiBEDEVConfigs, bedbrienvdevtblconfigs)
		self.Bind(wx.EVT_MENU, self.RiBEDEVDeviceids, bedbrienvdevtbldeviceids)
		self.Bind(wx.EVT_MENU, self.RiBEDEVLabs, bedbrienvdevtbllabs)
		self.Bind(wx.EVT_MENU, self.RiBEDEVLogs, bedbrienvdevtbllogs)
		self.Bind(wx.EVT_MENU, self.RiBEDEVPlatforms, bedbrienvdevtblplatforms)
		self.Bind(wx.EVT_MENU, self.RiBEDEVScreenshots, bedbrienvdevtblscreenshots)
		self.Bind(wx.EVT_MENU, self.RiBEDEVTitles, bedbrienvdevtbltitles)
		self.Bind(wx.EVT_MENU, self.RiBEDEVTOPTitles, bedbrienvdevtbltoptitles)
		self.Bind(wx.EVT_MENU, self.RiBEDEVAll, bedbrienvdevtblall)
		self.Bind(wx.EVT_MENU, self.RiBETSTBenchmarks, bedbrienvtsttblbenchmarks)
		self.Bind(wx.EVT_MENU, self.RiBETSTComments, bedbrienvtsttblcomments)
		self.Bind(wx.EVT_MENU, self.RiBETSTConfigs, bedbrienvtsttblconfigs)
		self.Bind(wx.EVT_MENU, self.RiBETSTDeviceids, bedbrienvtsttbldeviceids)
		self.Bind(wx.EVT_MENU, self.RiBETSTLabs, bedbrienvtsttbllabs)
		self.Bind(wx.EVT_MENU, self.RiBETSTLogs, bedbrienvtsttbllogs)
		self.Bind(wx.EVT_MENU, self.RiBETSTPlatforms, bedbrienvtsttblplatforms)
		self.Bind(wx.EVT_MENU, self.RiBETSTScreenshots, bedbrienvtsttblscreenshots)
		self.Bind(wx.EVT_MENU, self.RiBETSTTitles, bedbrienvtsttbltitles)
		self.Bind(wx.EVT_MENU, self.RiBETSTTOPTitles, bedbrienvtsttbltoptitles)
		self.Bind(wx.EVT_MENU, self.RiBETSTAll, bedbrienvtsttblall)
		self.Bind(wx.EVT_MENU, self.RiBEPRDBenchmarks, bedbrienvprdtblbenchmarks)
		self.Bind(wx.EVT_MENU, self.RiBEPRDComments, bedbrienvprdtblcomments)
		self.Bind(wx.EVT_MENU, self.RiBEPRDConfigs, bedbrienvprdtblconfigs)
		self.Bind(wx.EVT_MENU, self.RiBEPRDDeviceids, bedbrienvprdtbldeviceids)
		self.Bind(wx.EVT_MENU, self.RiBEPRDLabs, bedbrienvprdtbllabs)
		self.Bind(wx.EVT_MENU, self.RiBEPRDLogs, bedbrienvprdtbllogs)
		self.Bind(wx.EVT_MENU, self.RiBEPRDPlatforms, bedbrienvprdtblplatforms)
		self.Bind(wx.EVT_MENU, self.RiBEPRDScreenshots, bedbrienvprdtblscreenshots)
		self.Bind(wx.EVT_MENU, self.RiBEPRDTitles, bedbrienvprdtbltitles)
		self.Bind(wx.EVT_MENU, self.RiBEPRDTOPTitles, bedbrienvprdtbltoptitles)
		self.Bind(wx.EVT_MENU, self.RiBEPRDAll, bedbrienvprdtblall)
		
		self.Bind(wx.EVT_MENU, self.RiSSDevSS, ssdbrienvdevtblss)
		self.Bind(wx.EVT_MENU, self.RiSSDevBenchmarks, ssdbrienvdevtblssbenchmarks)
		self.Bind(wx.EVT_MENU, self.RiSSDevConfigs, ssdbrienvdevtblssconfigs)
		self.Bind(wx.EVT_MENU, self.RiSSDevDeviceids, ssdbrienvdevtblssdeviceids)
		self.Bind(wx.EVT_MENU, self.RiSSDevScreenshots, ssdbrienvdevtblssscreenshots)
		self.Bind(wx.EVT_MENU, self.RiSSDevThumbnails, ssdbrienvdevtblssthumbnails)
		self.Bind(wx.EVT_MENU, self.RiSSDevTitles, ssdbrienvdevtblsstitles)
		self.Bind(wx.EVT_MENU, self.RiSSDevAll, ssdbrienvdevtblall)
		self.Bind(wx.EVT_MENU, self.RiSSTstSS, ssdbrienvtsttblss)
		self.Bind(wx.EVT_MENU, self.RiSSTstBenchmarks, ssdbrienvtsttblssbenchmarks)
		self.Bind(wx.EVT_MENU, self.RiSSTstConfigs, ssdbrienvtsttblssconfigs)
		self.Bind(wx.EVT_MENU, self.RiSSTstDeviceids, ssdbrienvtsttblssdeviceids)
		self.Bind(wx.EVT_MENU, self.RiSSTstScreenshots, ssdbrienvtsttblssscreenshots)
		self.Bind(wx.EVT_MENU, self.RiSSTstThumbnails, ssdbrienvtsttblssthumbnails)
		self.Bind(wx.EVT_MENU, self.RiSSTstTitles, ssdbrienvtsttblsstitles)
		self.Bind(wx.EVT_MENU, self.RiSSTstAll, ssdbrienvtsttblall)
		self.Bind(wx.EVT_MENU, self.RiSSPrdSS, ssdbrienvprdtblss)
		self.Bind(wx.EVT_MENU, self.RiSSPrdBenchmarks, ssdbrienvprdtblssbenchmarks)
		self.Bind(wx.EVT_MENU, self.RiSSPrdConfigs, ssdbrienvprdtblssconfigs)
		self.Bind(wx.EVT_MENU, self.RiSSPrdDeviceids, ssdbrienvprdtblssdeviceids)
		self.Bind(wx.EVT_MENU, self.RiSSPrdScreenshots, ssdbrienvprdtblssscreenshots)
		self.Bind(wx.EVT_MENU, self.RiSSPrdThumbnails, ssdbrienvprdtblssthumbnails)
		self.Bind(wx.EVT_MENU, self.RiSSPrdTitles, ssdbrienvprdtblsstitles)
		self.Bind(wx.EVT_MENU, self.RiSSPrdAll, ssdbrienvprdtblall)
		self.Bind(wx.EVT_MENU, self.RiBERepoDev, reporiberepodev)
		self.Bind(wx.EVT_MENU, self.RiBERepoTst, reporiberepotst)
		self.Bind(wx.EVT_MENU, self.RiBERepoPrd, reporiberepoprd)
		self.Bind(wx.EVT_MENU, self.RiSSRepoDev, reporissrepodev)
		self.Bind(wx.EVT_MENU, self.RiSSRepoTst, reporissrepotst)
		self.Bind(wx.EVT_MENU, self.RiSSRepoPrd, reporissrepoprd)
		
		self.SetMenuBar(menubar)
		
		self.SetSize((350, 250))
		self.SetTitle('IGGE QA Tools')
		self.Center()
		self.Show(True)
		
	def OnQuit(self, e):
		self.Close()

	def BEDevN(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/traverse_gswsResults.py 1 n')
	
	def BEDevC(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/traverse_gswsResults.py 1 c')

	def BETstN(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/traverse_gswsResults.py 1 n')
	
	def BETstC(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/traverse_gswsResults.py 1 c')
		
	def BEPrdN(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/traverse_gswsResults.py 1 n')
	
	def BEPrdC(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/traverse_gswsResults.py 1 c')
		
	def SSDev(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/gswservice_api_call.py 1')
		
	def SSTst(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/gswservice_api_call.py 2')
	
	def SSPrd(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/gswservice_api_call.py 3')
		
	def VisVerify(self, e):
		ValFrame().Show()

	def RiBEDEVBenchmarks(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblBenchmarks.py 1')		
	def RiBEDEVComments(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblComments.py 1')		
	def RiBEDEVConfigs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblConfigs.py 1')		
	def RiBEDEVDeviceids(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tbldeviceids.py 1')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbldeviceids.py 1')
	def RiBEDEVLabs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLabs.py 1')
#		time.sleep(5)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbllabs.py 1')
	def RiBEDEVLogs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLogs.py 1')		
	def RiBEDEVPlatforms(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblPlatforms.py 1')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tblPlatforms.py 1')
	def RiBEDEVScreenshots(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblScreenShots.py 1')		
	def RiBEDEVTitles(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTitles.py 1')		
	def RiBEDEVTOPTitles(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTOPTitles.py 1')		
	def RiBEDEVAll(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblBenchmarks.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblComments.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblConfigs.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tbldeviceids.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLabs.py 1')
		time.sleep(3)		
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLogs.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblPlatforms.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblScreenShots.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTitles.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTOPTitles.py 1')
		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbllabs.py 1')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tblPlatforms.py 1')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbldeviceids.py 1')
		
	
	def RiBETSTBenchmarks(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblBenchmarks.py 2')		
	def RiBETSTComments(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblComments.py 2')		
	def RiBETSTConfigs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblConfigs.py 2')		
	def RiBETSTDeviceids(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tbldeviceids.py 2')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbldeviceids.py 2')
	def RiBETSTLabs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLabs.py 2')
#		time.sleep(5)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbllabs.py 2')
	def RiBETSTLogs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLogs.py 2')		
	def RiBETSTPlatforms(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblPlatforms.py 2')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tblPlatforms.py 2')
	def RiBETSTScreenshots(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblScreenShots.py 2')		
	def RiBETSTTitles(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTitles.py 2')		
	def RiBETSTTOPTitles(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTOPTitles.py 2')		
	def RiBETSTAll(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblBenchmarks.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblComments.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblConfigs.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tbldeviceids.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLabs.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLogs.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblPlatforms.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblScreenShots.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTitles.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTOPTitles.py 2')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbllabs.py 2')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tblPlatforms.py 2')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbldeviceids.py 2')
	
	def RiBEPRDBenchmarks(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblBenchmarks.py 3')		
	def RiBEPRDComments(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblComments.py 3')		
	def RiBEPRDConfigs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblConfigs.py 3')		
	def RiBEPRDDeviceids(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tbldeviceids.py 3')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbldeviceids.py 3')
	def RiBEPRDLabs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLabs.py 3')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbllabs.py 3')
	def RiBEPRDLogs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLogs.py 3')		
	def RiBEPRDPlatforms(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblPlatforms.py 3')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tblPlatforms.py 3')
	def RiBEPRDScreenshots(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblScreenShots.py 3')		
	def RiBEPRDTitles(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTitles.py 3')		
	def RiBEPRDTOPTitles(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTOPTitles.py 3')		
	def RiBEPRDAll(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblBenchmarks.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblComments.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblConfigs.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tbldeviceids.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLabs.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblLogs.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblPlatforms.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblScreenShots.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTitles.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/create_tblTOPTitles.py 3')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbllabs.py 3')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tblPlatforms.py 3')
#		time.sleep(3)
#		os.system('start python D:/Projects/IGGE/python_scripts/backend/db_maint_scripts/create_db/run_once/populate_tbldeviceids.py 3')
		
	def RiSSDevSS(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSnapshots.py 1')
	def RiSSDevBenchmarks(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSBenchmarks.py 1')
	def RiSSDevConfigs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSConfigs.py 1')
	def RiSSDevDeviceids(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSDeviceIds.py 1')
	def RiSSDevScreenshots(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSScreenShots.py 1')
	def RiSSDevThumbnails(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSThumbnails.py 1')
	def RiSSDevTitles(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSTitles.py 1')
	def RiSSDevAll(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSnapshots.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSBenchmarks.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSConfigs.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSDeviceIds.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSScreenShots.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSThumbnails.py 1')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSTitles.py 1')
		time.sleep(3)
		
	def RiSSTstSS(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSnapshots.py 2')
	def RiSSTstBenchmarks(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSBenchmarks.py 2')
	def RiSSTstConfigs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSConfigs.py 2')
	def RiSSTstDeviceids(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSDeviceIds.py 2')
	def RiSSTstScreenshots(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSScreenShots.py 2')
	def RiSSTstThumbnails(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSThumbnails.py 2')
	def RiSSTstTitles(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSTitles.py 2')
	def RiSSTstAll(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSnapshots.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSBenchmarks.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSConfigs.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSDeviceIds.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSScreenShots.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSThumbnails.py 2')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSTitles.py 2')
		time.sleep(3)
		
	def RiSSPrdSS(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSnapshots.py 3')
	def RiSSPrdBenchmarks(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSBenchmarks.py 3')
	def RiSSPrdConfigs(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSConfigs.py 3')
	def RiSSPrdDeviceids(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSDeviceIds.py 3')
	def RiSSPrdScreenshots(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSScreenShots.py 3')
	def RiSSPrdThumbnails(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSThumbnails.py 3')
	def RiSSPrdTitles(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSTitles.py 3')
	def RiSSPrdAll(self, e):
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSnapshots.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSBenchmarks.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSConfigs.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSDeviceIds.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSScreenShots.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSThumbnails.py 3')
		time.sleep(3)
		os.system('start python D:/Projects/IGGE/python_scripts/snapshot/db_maint_scripts/create_db/run_once/create_tblSSTitles.py 3')
		time.sleep(3)
		
#	def Ri<BU>localRepo(self, e):
	def RiBERepoDev(self, e):
		r_path = 'D:/Projects/IGGE/repo/BERepo/Dev/'
		if os.path.exists(r_path):
			filelist = os.listdir(r_path)
			for file in filelist:
				if not os.path.isfile(r_path + file):
					shutil.rmtree(r_path + file)
					
	def RiBERepoTst(self, e):
		r_path = 'D:/Projects/IGGE/repo/BERepo/Test/'
		if os.path.exists(r_path):
			filelist = os.listdir(r_path)
			for file in filelist:
				if not os.path.isfile(r_path + file):
					shutil.rmtree(r_path + file)

	def RiBERepoPrd(self, e):
		r_path = 'D:/Projects/IGGE/repo/BERepo/Prd/'
		if os.path.exists(r_path):
			filelist = os.listdir(r_path)
			for file in filelist:
				if not os.path.isfile(r_path + file):
					shutil.rmtree(r_path + file)
					
	def RiSSRepoDev(self, e):
		r_path = 'D:/Projects/IGGE/repo/SSRepo/Dev/'
		if os.path.exists(r_path):
			filelist = os.listdir(r_path)
			for file in filelist:
				if not os.path.isfile(r_path + file):
					shutil.rmtree(r_path + file)
		
	def RiSSRepoTst(self, e):
		r_path = 'D:/Projects/IGGE/repo/SSRepo/Test/'
		if os.path.exists(r_path):
			filelist = os.listdir(r_path)
			for file in filelist:
				if not os.path.isfile(r_path + file):
					shutil.rmtree(r_path + file)		
	
	def RiSSRepoPrd(self, e):
		r_path = 'D:/Projects/IGGE/repo/SSRepo/Prd/'
		if os.path.exists(r_path):
			filelist = os.listdir(r_path)
			for file in filelist:
				if not os.path.isfile(r_path + file):
					shutil.rmtree(r_path + file)				

class MyImageRenderer(wx.grid.PyGridCellRenderer):
	def __init__(self, img):
	 wx.grid.PyGridCellRenderer.__init__(self)
	 self.img = img
	def Draw(self, grid, attr, dc, rect, row, col, isSelected):
	 image = wx.MemoryDC()
	 image.SelectObject(self.img)
	 dc.SetBackgroundMode(wx.SOLID)
	 if isSelected:
		 dc.SetBrush(wx.Brush(wx.BLUE, wx.SOLID))
		 dc.SetPen(wx.Pen(wx.BLUE, 1, wx.SOLID))
	 else:
		 dc.SetBrush(wx.Brush(wx.WHITE, wx.SOLID))
		 dc.SetPen(wx.Pen(wx.WHITE, 1, wx.SOLID))
	 dc.DrawRectangleRect(rect)
	 width, height = self.img.GetWidth(), self.img.GetHeight()
	 if width > rect.width-2:
		 width = rect.width-2
	 if height > rect.height-2:
		 height = rect.height-2
	 dc.Blit(rect.x+1, rect.y+1, width, height, image, 0, 0, wx.COPY, True)
					
def main():
	app = wx.App()
	MainFrame(None)
	app.MainLoop()
	
if __name__=='__main__':
	main()
