import maya.cmds as cmds

class ChangeBornSize(object):

    def __init__(self):
        self.windowID = 'window_set_joint_size'
        self.sliderID = 'slider_set_joint_size'
        self.radioID = 'radio_set_joint_size'
        self.title = 'title_set joint size'
        self.size = (500, 50)
        self.mode = 0
        '''
        mode = 0    change size object born
        mode = 1    change size hierarchy object born
        mode = 2    change size all object born
        '''

    def deleteUICmd(self, *args):
        cmds.deleteUI(self.windowID, window = True)

    def applyCmd(self, *args):

        if self.mode == 0:

            cmds.select()
            self.selected_object = cmds.ls(selection = True)

            if not self.selected_object:
                print('Please select born')
            else:
                self.jointSize = cmds.floatSliderGrp(self.sliderID, query = True, value = True)
                for node in self.selected_object:
                    if cmds.nodeType(node) == 'joint':
                        cmds.setAttr(node + '.radius', self.jointSize)
                cmds.select(clear = True)
                cmds.select(self.selected_object)


        elif self.mode == 1:

            cmds.select(hierarchy = True)
            self.selected_object = cmds.ls(selection = True)

            if not self.selected_object:
                print('Please select born')
            else:
                self.first_object = self.selected_object[0]
                self.jointSize = cmds.floatSliderGrp(self.sliderID, query = True, value = True)
                for node in self.selected_object:
                    if cmds.nodeType(node) == 'joint':
                        cmds.setAttr(node + '.radius', self.jointSize)
                cmds.select(clear = True)
                cmds.select(self.selected_object, hierarchy = True)

        else:
            cmds.select()
            self.selected_object = cmds.ls(selection = True)

            if not self.selected_object:
                print('Please select born')
            else:
                check = self.selected_object[0]
                while(True):
                    obj = cmds.pickWalk(direction = 'up')
                    if check == obj:
                        break
                    else:
                        check = obj

                cmds.select(check, hierarchy = True)
                self.selected_object = cmds.ls(selection = True)
                self.jointSize = cmds.floatSliderGrp(self.sliderID, query = True, value = True)
                for node in self.selected_object:
                    if cmds.nodeType(node) == 'joint':
                        cmds.setAttr(node + '.radius', self.jointSize)

                cmds.select(clear = True)
                cmds.select(check)

    def changeMode0(self, *args):
        self.mode = 0

    def changeMode1(self, *args):
        self.mode = 1

    def changeMode2(self, *args):
        self.mode = 2

    def createUI(self):

        if cmds.window(self.windowID, exists = True):
            self.deleteUICmd()

        self.window = cmds.window(self.windowID,
                              title = self.title,
                              menuBar = True,
                              sizeable = False,
                              widthHeight = self.size
                              )
        cmds.menu(label = 'Mode')
        self.modeMenuRadio = cmds.radioMenuItemCollection()
        cmds.menuItem(label = 'Full',
                      radioButton = True,
                      command = self.changeMode2
                      )
        cmds.menuItem(label = 'hierarchy',
                      radioButton = True,
                      command = self.changeMode1
                      )
        cmds.menuItem(label = 'selected',
                      radioButton = True,
                      command = self.changeMode0
                      )
        cmds.menu(label = 'Help')
        cmds.menuItem(label = 'don\'t rely on help')
        cmds.columnLayout()
        cmds.rowLayout(numberOfColumns = 3)
#         cmds.text(label = 'Change joint size')
        cmds.floatSliderGrp(self.sliderID,
                            field = True,
                            value = 1,
                            min = 0,
                            max = 5,
                            fieldMinValue = 0,
                            fieldMaxValue = 50,
                            label = 'joint size',
                            changeCommand = self.applyCmd
                            )
        cmds.button(label = 'apply', command = self.applyCmd)
        cmds.button(label = 'close', command = self.deleteUICmd)
        cmds.showWindow(self.windowID)

window = ChangeBornSize()
window.createUI()
