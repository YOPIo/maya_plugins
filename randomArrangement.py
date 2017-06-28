import maya.cmds as cmds
import random

class RandomArrange(object):

    def __init__(self):
        self.windowID = 'randomArrange'
        self.title= 'Random Arrangement'
        self.size = (546, 350)
        self.copy_mode = True
        '''
        True -> Normal
        False -> Instance
        '''
        self.copy = 5
        self.translate = [0, 0, 0]
        self.rotate = [0, 0, 0]
        self.scale = [0, 0, 0]

    def createWindow(self):
        if cmds.window(self.windowID, exists = True):
            cmds.deleteUI(self.windowID, window = True)

        self.windowID = cmds.window(
                                  self.windowID,
                                  title = self.title,
                                  widthHeight = self.size,
                                  menuBar = True
                                  )
        self.mainForm = cmds.formLayout(numberOfDivisions = 100)
        #self.createMenu()
        self.createButton()
        self.optionsBorder = cmds.tabLayout(scrollable = True,
                                            tabsVisible = False,
                                            height = 1,
                                            childResizable = True
                                            )
        cmds.formLayout(self.mainForm,
                        e = True,
                        attachForm = (
                                      [self.optionsBorder, 'top', 1],
                                      [self.optionsBorder, 'left', 2],
                                      [self.optionsBorder, 'right', 2]
                                      ),
                        attachControl = ([self.optionsBorder, 'bottom', 5, self.applyBtn])
                        )
        self.optionsForm = cmds.formLayout(numberOfDivisions = 100)
        self.createMainForm()
        cmds.showWindow()

    def applyAndCloseCmd(self, *args):
        self.applyCmd()
        self.closeCmd()

    def applyCmd(self, *args):

        self.selected_object = cmds.ls(selection = True)
        if len(self.selected_object) <= 0:
            exit('Please select object')

        cmds.select(clear = True)
        self.n = cmds.intFieldGrp(self.number, q = True, value = True)
        self.forN = self.n[0]
        if(self.forN <= 0):
            exit('Number Error!')

        for i in range(self.forN):
            self.calRand()
            if self.copy_mode:
                self.duplicated_object = cmds.duplicate(self.selected_object, returnRootsOnly = True)
            else:
                self.duplicated_object = cmds.instance(self.selected_object)
            cmds.select(self.duplicated_object, add = True)
            cmds.xform(self.duplicated_object,
                       translation = [self.rxTrans, self.ryTrans, self.rzTrans],
                       rotation = [self.rxRotate, self.ryRotate, self.rzRotate],
                       scale = [self.rxScale, self.ryScale, self.rzScale]
                       )

    def onCmdRelative(self, *args):
        print 'Relative mode'
        self.arrange_mode = True

    def onCmdAbsolute(self, *args):
        print 'Absolute mode'
        self.arrange_mode = False

    def onCmdNormal(self, *args):
        print 'Normal copy mode'
        self.copy_mode = True

    def onCmdInstance(self, *args):
        print 'Instance copy mode'
        self.copy_mode = False


    def closeCmd(self, *args):
        cmds.deleteUI(self.windowID, window = True)

    def calRand(self):

        self.flag = False
        for i in self.n:
            xTrans = cmds.floatFieldGrp(self.xTrans, q = True, value = True)
            if xTrans[0] > xTrans[1]:
                print 'x translate error'
                self.flag = True
            yTrans = cmds.floatFieldGrp(self.yTrans, q = True, value = True)
            if yTrans[0] > yTrans[1]:
                print 'y translate error'
                self.flag = True
            zTrans = cmds.floatFieldGrp(self.zTrans, q = True, value = True)
            if zTrans[0] > zTrans[1]:
                print 'z translate error'
                self.flag = True
            xRotate = cmds.floatFieldGrp(self.xRotate, q = True, value = True)
            if xRotate[0] > xRotate[1]:
                print 'x Rotate error'
                self.flag = True
            yRotate = cmds.floatFieldGrp(self.yRotate, q = True, value = True)
            if yRotate[0] > yRotate[1]:
                print 'y Rotate error'
                self.flag = True
            zRotate = cmds.floatFieldGrp(self.zRotate, q = True, value = True)
            if zRotate[0] > zRotate[1]:
                print 'z Rotate error'
                self.flag = True

            xScale = cmds.floatFieldGrp(self.xScale, q = True, value = True)
            if xScale[0] > xScale[1]:
                print 'x Scale error'
                self.flag = True
            yScale = cmds.floatFieldGrp(self.yScale, q = True, value = True)
            if yScale[0] > yScale[1]:
                print 'y Scale error'
                self.flag = True
            zScale = cmds.floatFieldGrp(self.zScale, q = True, value = True)
            if zScale[0] > zScale[1]:
                print 'z Scale error'
                self.flag = True

            random.seed()
            self.rxTrans = random.uniform(xTrans[0], xTrans[1])
            self.ryTrans = random.uniform(yTrans[0], yTrans[1])
            self.rzTrans = random.uniform(zTrans[0], zTrans[1])
            self.rxRotate = random.uniform(xRotate[0], xRotate[1])
            self.ryRotate = random.uniform(yRotate[0], yRotate[1])
            self.rzRotate = random.uniform(zRotate[0], zRotate[1])
            self.rxScale = random.uniform(xScale[0], xScale[1])
            self.ryScale = random.uniform(yScale[0], yScale[1])
            self.rzScale = random.uniform(zScale[0], zScale[1])

            print self.rzScale

            if self.flag:
                exit('Number Error!')


    def createMainForm(self):
        self.radioMode = cmds.radioButtonGrp(label = 'Copy Options : ',
                                             labelArray2 = ['Normal',
                                                            'Instance'],
                                             numberOfRadioButtons = 2,
                                             select = 1,
                                             onCommand1 = self.onCmdNormal,
                                             onCommand2 = self.onCmdInstance,
                                             )

        self.number = cmds.intFieldGrp(label = 'Number of copies', value = [5, 1, 1, 1])
        cmds.formLayout(self.optionsForm,
                        e = True,
                        attachControl = ([self.number, 'top', 10, self.radioMode])
                        )

        self.xTrans = cmds.floatFieldGrp(label = 'Translate X [min, max]',
                                         numberOfFields = 2
                                         )
        cmds.formLayout(self.optionsForm,
                        e = True,
                        attachControl = ([self.xTrans, 'top', 10, self.number])
                        )
        self.yTrans = cmds.floatFieldGrp(label = 'Translate Y [min, max]',
                                         numberOfFields = 2
                                         )
        cmds.formLayout(self.optionsForm,
                        e = True,
                        attachControl = ([self.yTrans, 'top', 2, self.xTrans]),
                        )
        self.zTrans = cmds.floatFieldGrp(label = 'Translate Z [min, max]',
                                         numberOfFields = 2
                                         )
        cmds.formLayout(self.optionsForm,
                        e = True,
                        attachControl = ([self.zTrans, 'top', 2, self.yTrans])
                        )

        self.xRotate = cmds.floatFieldGrp(label = 'Rotate X [min, max]',
                                         numberOfFields = 2
                                         )
        cmds.formLayout(self.optionsForm,
                        e = True,
                        attachControl = ([self.xRotate, 'top', 10, self.zTrans])
                        )
        self.yRotate = cmds.floatFieldGrp(label = 'Rotate Y [min, max]',
                                         numberOfFields = 2
                                         )
        cmds.formLayout(self.optionsForm,
                        e = True,
                        attachControl = ([self.yRotate, 'top', 2, self.xRotate])
                        )
        self.zRotate = cmds.floatFieldGrp(label = 'Rotate Z [min, max]',
                                         numberOfFields = 2
                                         )
        cmds.formLayout(self.optionsForm,
                        e = True,
                        attachControl = ([self.zRotate, 'top', 2, self.yRotate])
                        )

        self.xScale = cmds.floatFieldGrp(label = 'Slace X [min, max]',
                                         numberOfFields = 2,
                                         value = [1.0, 1.0, 1.0, 1.0]
                                         )
        cmds.formLayout(self.optionsForm,
                        e = True,
                        attachControl = ([self.xScale, 'top', 10, self.zRotate])
                        )
        self.yScale = cmds.floatFieldGrp(label = 'Scale Y [min, max]',
                                         numberOfFields = 2,
                                         value = [1.0, 1.0, 1.0, 1.0]
                                         )
        cmds.formLayout(self.optionsForm,
                        e = True,
                        attachControl = ([self.yScale, 'top', 2, self.xScale])
                        )
        self.zScale = cmds.floatFieldGrp(label = 'Scale Z [min, max]',
                                         numberOfFields = 2,
                                         value = [1.0, 1.0, 1.0, 1.0]
                                         )
        cmds.formLayout(self.optionsForm,
                        e = True,
                        attachControl = ([self.zScale, 'top', 2, self.yScale])
                        )




    def createButton(self):
        self.btnSize = ((self.size[0] - 18) / 3, 26)
        self.applyAndCloseBtn = cmds.button(label = 'Apply and Close',
                                            height = self.btnSize[1],
                                            command = self.applyAndCloseCmd
                                            )
        self.applyBtn = cmds.button(label = 'Apply',
                                    height = self.btnSize[1],
                                    command = self.applyCmd
                                    )
        self.closeBtn = cmds.button(label = 'Close',
                                    height = self.btnSize[1],
                                    command = self.closeCmd
                                    )
        cmds.formLayout(self.mainForm,
                        e = True,
                        attachForm = ([self.applyAndCloseBtn, 'left', 5],
                                      [self.applyAndCloseBtn, 'bottom', 5],
                                      [self.applyBtn, 'bottom', 5],
                                      [self.closeBtn, 'bottom', 5],
                                      [self.closeBtn, 'right', 5]
                                      ),
                        attachPosition = ([self.applyAndCloseBtn, 'right', 1, 33],
                                          [self.closeBtn, 'left', 0, 67]
                                          ),
                        attachControl = ([self.applyBtn, 'left', 4, self.applyAndCloseBtn],
                                         [self.applyBtn, 'right', 4, self.closeBtn]
                                         ),
                        attachNone = ([self.applyAndCloseBtn, 'top'],
                                      [self.applyBtn, 'top'],
                                      [self.closeBtn, 'top']
                                      )
                        )

win = RandomArrange()
win.createWindow()