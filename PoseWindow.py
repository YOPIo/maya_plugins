import maya.cmds as cmds
import maya.mel as mel
import os, cPickle, sys

kPoseFileExtension = 'pse'

class MainWindow(object):
    """this class is for main window"""
    @classmethod
    def __init__(self):
        self.window = "PoseManagerWindow"
        self.title = "Pose Manager"
        self.size = (300, 150)

        if mel.eval('getApplicationVersionAsFloat()') > 2010.0:
            self.size = (300, 150)

        self.tempFile = os.path.join(
            os.path.expanduser('~'),
            'temp_pose.%s'%kPoseFileExtension
        )

        self.clipboardStat = 'No pose currently copied.'
        if (os.path.exists(self.tempFile)):
            self.clipboardStat = 'Old pose currently copied to clipboard.'

        self.fileFilter = 'Pose (*.%s)'%kPoseFileExtension

    def create(self):
        """create a window"""
        if(cmds.window(self.window, exists = True)):
            cmds.deleteUI(self.window, window = True)

        #initalize the window
        self.window = cmds.window(
                                  self.window,
                                  title = self.title,
                                  widthHeight = self.size,
                                  menuBar = True,
                                  sizeable = False
                                  )
        self.mainForm = cmds.formLayout(numberOfDivisions = 100)
        #create Menu Bar
        self.makeMenuBtn()
        #create buttons
        self.createBtn()
        #show window
        cmds.showWindow()



    def createBtn(self):
        self.frame = cmds.frameLayout(
                                      parent = self.mainForm,
                                      label = "Click Copy button or Paste button",
                                      width = self.size[0] - 3,
                                      borderVisible = True
                                      )
        self.upperLayout = cmds.rowLayout(numberOfColumns = 2)
        self.copyBtn = cmds.button(
                                   label = "Copy",
                                   command = self.copyCmd,
                                   width = (self.size[0] - 9) / 2,
                                   height = 50
                                   )
        self.pasteBtn = cmds.button(
                                    label = "Paste",
                                    command = self.pasteCmd,
                                    width = (self.size[0] - 9) / 2,
                                    height =50
                                    )

        self.resultLayout = cmds.frameLayout(
                                             parent = self.mainForm,
                                             label = "result",
                                             width = self.size[0] - 3,
                                             borderVisible = True
                                             )
        self.underLayout= cmds.rowLayout(numberOfColumns = 2)
        self.outputText = cmds.text(
                                    width = self.size[0] - 48,
                                    height = 30,
                                    label = "result"
                                    )
        self.closeBtn = cmds.button(
                                    label = "close",
                                    command = self.closeCmd
                                    )

        cmds.formLayout(
                        self.mainForm,
                        edit = True,
                        attachControl = ([self.resultLayout, 'top', 0, self.frame])

                        )




    def makeMenuBtn(self):
        self.fileMenu = cmds.menu(label = "File")
        self.saveMenu = cmds.menuItem(
                                      label = "Save a animation",
                                      command = self.saveCmd
                                      )
        self.loadMenu = cmds.menuItem(
                                      label = "Load a animation",
                                      command = self.loadCmd
                                      )

        self.helpMenu = cmds.menu(label = "Help")
        self.helpItem = cmds.menuItem(label = "Don't rely on Help!!")

    def closeBtn(self):
        self.closeLayout = cmds.formLayout(parent = self.mainForm)
        self.closeBtn = cmds.button(
                                    label = "close",
                                    command = self.closeCmd
                                    )

    def getSelection(self):
        rootNodes = cmds.ls(sl=True, type = 'transform')
        if rootNodes is None or len(rootNodes) < 1:
            cmds.confirmDialog(t ='Error', b = ['OK'],
                m = 'Please select one or more transform nodes.')
            return None
        else: return rootNodes


    def copyCmd(self, *args):
        rootNode = self.getSelection()

        if rootNode is None: return

        cmds.text(
                  self.outputText,
                  edit = True,
                  label = "Copied"
                  )
        exportFile(self.tempFile, rootNode)

    def pasteCmd(self, *args):
        if not os.path.exists(self.tempFile): return
        importFile(self.tempFile)

        obj = cmds.ls(sl = True)
        cmds.select(obj, hierarchy = True)
        cmds.text(
                  self.outputText,
                  edit = True,
                  label = "Pasted. You can set keies"
                  )


    def saveCmd(self, *args):
        rootNode = self.getSelection()
        if rootNode is None: return

        filePath = ""

        try:
            filePath = cmds.fileDialog2(
                                        ff = self.fileFilter,
                                        fileMode = 0
                                        )
        except:
            filePath = cmds.fileDialog(
                                       dm = '*.%s'%kPoseFileExtension, mode=1
                                       )

        if filePath is None or len(filePath) < 1:
            return
        if isinstance(filePath, list):
            filePath = filePath[0]
        exportFile(filePath, cmds.ls(sl = True, type = 'transform'))

    def loadCmd(self, *args):

        filePath = ''
        try:
            filePath = cmds.fileDialog2(
                ff=self.fileFilter, fileMode=1
            )
        except:
            filePath = cmds.fileDialog(
                dm='*.%s'%kPoseFileExtension, mode=0
            )

        if filePath is None or len(filePath) < 1: return
        if isinstance(filePath, list): filePath = filePath[0]
        importFile(filePath)

    def closeCmd(self, *args):
        cmds.deleteUI(self.window, window = True)


def exportFile(filePath, rootNode):

    try: f = open(filePath, 'w')
    except:
        cmds.confirmDialog(
            t='Error', b=['OK'],
            m='Unable to write file: %s'%filePath
        )
        raise
    data = saveHiearchy(rootNode, [])
    cPickle.dump(data, f)
    f.close()

def saveHiearchy(rootNode, data):

    for node in rootNode:
        nodeType = cmds.nodeType(node)
        if not (nodeType=='transform' or
            nodeType=='joint'): continue
        keyableAttrs = cmds.listAttr(node, keyable=True)
        if keyableAttrs is not None:
            for attr in keyableAttrs:
                data.append(['%s.%s'%(node,attr), cmds.getAttr('%s.%s'%(node,attr))])

        children = cmds.listRelatives(node, children=True)
        if children is not None: saveHiearchy(children, data)
    return data

def importErrorWindow(errAttr):
    win = "ErrorWindow"

    def dismiss(*args):
        cmds.deleteUI(win, window = True)

    if(cmds.window(win, exists = True)):
        dismiss()

    size = (300, 200)
    cmds.window(win, widthHeight = size, title = 'Error Attribute', s = False)
    mainForm = cmds.formLayout()
    infoLbl = cmds.text(l='The following attributes could not be found.\nThey are being ignored.', al='left')
    scroller = cmds.scrollLayout(w=size[0])
    errStr = ''.join('\t- %s\n'%a for a in errAttr).rstrip()
    cmds.text(l=errStr, al='left')
    btn = cmds.button(l='OK', c=dismiss, p=mainForm, h=26)

    ac = []; af=[];
    ac.append([scroller,'top',5,infoLbl])
    ac.append([scroller,'bottom',5,btn])
    af.append([infoLbl,'top',5])
    af.append([infoLbl,'left',5])
    af.append([infoLbl,'right',5])
    af.append([scroller,'left',0])
    af.append([scroller,'right',0])
    af.append([btn,'left',5])
    af.append([btn,'right',5])
    af.append([btn,'bottom',5])
    cmds.formLayout(
        mainForm, e=True,
        attachControl=ac, attachForm=af
    )

    cmds.window(win, e=True, wh=size)
    cmds.showWindow(win)

def importFile(filePath):

    try: f = open(filePath, 'r')
    except:
        cmds.confirmDialog(
            t='Error', b=['OK'],
            m='Unable to open file: %s'%filePath
        )
        raise

    pose = cPickle.load(f)
    f.close()

    errAttrs = []
    for attrValue in pose:
        try: cmds.setAttr(attrValue[0], attrValue[1])
        except:
            try: errAttrs.append(attrValue[0])
            except: errAttrs.append(attrValue)

    if len(errAttrs) > 0:
        importErrorWindow(errAttrs)
        sys.stderr.write('Not all attributes could be loaded.')



win = MainWindow()
win.create()
