import maya.cmds as cmds

class NameChange(object):

    def __init__(self):
        self.window = 'namechangewindow'
        self.subWindow = 'subWindow'
        self.title = 'Change Name'
        self.subTitle = 'Enter name'
        self.textscroll = 'textScrollList'
        self.focus = 'textFocus'
        self.list = None
        self.setText = None
        self.size = (300, 550)
        self.subSize = (290, 30)

    def createUI(self):
        if cmds.window(self.window, exists = True):
            cmds.deleteUI(self.window, window = True)
        self.window = cmds.window(self.window, title = self.title, width = self.size[0], height = self.size[1], sizeable = False)
        self.layout = cmds.columnLayout()
        self.reroadButton = cmds.button(label = 'Reload', command = self.reloadCmd)
        cmds.textScrollList(self.textscroll, numberOfRows = 14, doubleClickCommand = self.doubleClickCmd)
        cmds.showWindow()

    def reloadCmd(self, *args):
        if self.list > 0:
            for i in self.list:
                self.list.remove(i)
        self.list = cmds.ls(selection = True)
        cmds.textScrollList(self.textscroll, e = True, removeAll = True)
        cmds.textScrollList(self.textscroll, e = True, append = self.list)

    def doubleClickCmd(self, *args):
        if cmds.window(self.subWindow, exists = True):
            cmds.deleteUI(self.subWindow, window = True)
        self.subWindow = cmds.window(self.subWindow, title = self.subTitle, width = self.subSize[0], height = self.subSize[1])
        self.subLayout = cmds.rowColumnLayout(numberOfColumns = 1)
        self.text = cmds.textField(self.focus, width = 280, enterCommand = self.applyCmd)
        cmds.setFocus(self.focus)
        cmds.showWindow()

    def applyCmd(self, *args):
        self.setText = cmds.textField(self.text, query = True, text = True)
        print self.setText
        cmds.deleteUI(self.subWindow, window = True)

win = NameChange()
win.createUI()





