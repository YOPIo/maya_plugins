import maya.cmds as cmds
import maya.OpenMaya as om

class CopyComponent():

    def __init__(self):
        pass

    def copy_component(self, *args):
        self.objects = cmds.ls(selection = True)
        print self.objects
        if len(self.objects) == 2:
            self.translation = cmds.xform(self.objects[0], query = True, translation = True)
            self.rotation = cmds.xform(self.objects[0], query = True, rotation = True)
            self.scale = cmds.xform(self.objects[0], query = True, scale = True)
            cmds.xform(self.objects[1], translation = self.translation)
            cmds.xform(self.objects[1], rotation = self.rotation)
            cmds.xform(self.objects[1], scale = self.scale)
        else:
             om.MGlobal.displayError('Please select two ojbects\n');

CopyComponent().copy_component()
