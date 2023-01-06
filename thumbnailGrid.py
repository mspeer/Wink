import wx
from wx.lib.pubsub import pub 
import wx.grid as gridlib
import os
import MySQLdb as mdb
 
########################################################################
class thmbDetailFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY, "Thumbnail Detail View")
        panel = wx.Panel(self)

        taskid = ''
 
        btn = wx.Button(self, label="Close Thumbnail Detail View")
        btn.Bind(wx.EVT_BUTTON, self.onClosethmbDetailFrame)
 
        pub.subscribe(self.thmbDetailListener, "detailpanelListener")
 
           #----------------------------------------------------------------------
    def thmbDetailListener(self, message, arg2=None):
        """
        Listener function
        """
        print "thmbDetailFrame: Received the following message: " + message
        self.taskid = message
        if arg2:
            print "thmbDetailFrame: Received another arguments: " + str(arg2)

    def onClosethmbDetailFrame(self, event):
        """
        Closes secondary frame
       """
#        frame = thmbGridFrame()
#        frame.Show()
 
#        msg = self.msgTxt.GetValue()
        msg = self.taskid
        print 'self.taskid:',self.taskid
        pub.sendMessage("gridpanelListener", message=msg)
        #pub.sendMessage("gridpanelListener", message="test3", arg2="2nd argument!")
        self.Close()
 
   
########################################################################
class thmbGridPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)


########################################################################
class thmbGridFrame(wx.Frame):
    """"""
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Thumbnail Grid View")
        panel = wx.Panel(self)
        pub.subscribe(self.thmbGridListener, "gridpanelListener")
        conbe = mdb.connect('localhost', 'root', '_PW_', 'iggebedbdev')
        cursor = conbe.cursor()     
        sql = 'SELECT DISTINCT tbltitles.name, tblbenchmarks.gameID FROM tbltitles \
                JOIN tblbenchmarks ON tbltitles.titleID = tblbenchmarks.titleID \
                WHERE tbltitles.thmb_vis_verified=0 \
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
        env = 'Dev'
        self.thmbmap = {}
        for row in rows:
            gname = row[0]
            self.taskid = str(row[1])
            if gname.find(':') or gname.find('/'):
                for ch in [':','/']:
                    if ch in gname:
                        gname = gname.replace(ch,"")
            thmbpath = 'D:\\Projects\\IGGE\\repo\\BERepo\\' + env + '\\' + gname + '\\RTM\\' + str(row[1]) + '\\thumbnail\\'
            img = wx.Bitmap(thmbpath+str(self.taskid)+'.jpg', wx.BITMAP_TYPE_JPEG)
            imageRenderer = MyImageRenderer(img)
            self.myGrid.SetCellRenderer(currow,curcol,imageRenderer)
            self.myGrid.SetColSize(curcol,img.GetWidth()+2)
            self.myGrid.SetRowSize(currow,img.GetHeight()+2)
            self.thmbmap[str(currow)+"_"+str(curcol)] = self.taskid
            print 'thmbmap:', self.thmbmap[str(currow)+"_"+str(curcol)]
            curcol = curcol + 1
            if curcol > 2:
                curcol = 0
                currow = currow + 1
        self.myGrid.GetGridWindow().Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(myGrid)
        panel.SetSizer(sizer)
        self.Show()

    def OnRightClick(self, event):
        x, y = self.myGrid.CalcUnscrolledPosition(event.GetX(), event.GetY())
        row, col = self.myGrid.XYToCell(x, y)
#       print row,col
        taskid = self.thmbmap[str(row) + "_" + str(col)]
        print "taskid:", taskid
        frame = thmbDetailFrame()
        frame.Show()
        msg = taskid
        pub.sendMessage("detailpanelListener", message=msg)
        #pub.sendMessage("detailpanelListener", message="test2", arg2="2nd argument!")
#       self.Close()   

    def thmbGridListener(self, message, arg2=None):
        """
        Listener function
        """
        print "thmbGridFrame: Received the following message: " + message
        if arg2:
            print "thmbGridFrame: Received another arguments: " + str(arg2)

 
   #----------------------------------------------------------------------
#    def onOpenthmbDetailFrame(self, event):
#       """
#        Opens secondary frame
#       """
#        frame = thmbDetailFrame()
#        frame.Show()
# 
##        msg = self.msgTxt.GetValue()
#        msg = 'taskID: 6896'
#        pub.sendMessage("detailpanelListener", message=msg)
#        pub.sendMessage("detailpanelListener", message="test2", arg2="2nd argument!")
##       self.Close()

#----------------------------------------------------------------------

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

#if __name__ == "__main__":
#    app = wx.App(False)
#    frame = thmbGridFrame()
#    app.MainLoop()

def run():
    app = wx.App()
    app.SetAppName('thumbnailGrid')
    thmbGridframe = thmbGridFrame()
    thmbGridframe.Show()
    app.MainLoop()
