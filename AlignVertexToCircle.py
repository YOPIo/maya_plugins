import pymel.core as pm
from math import *
import sys

sys.dont_write_bytecode = True

def AlignVertexOnCircle(axis,mode,sp):
    space=['object','world'][sp]
    
    if not pm.selected():
        return
    pm.runtime.ConvertSelectionToVertices(pm.selected(flatten=True))
    vtxList = pm.filterExpand(selectionMask=31)
    if len(vtxList)<3:
        return
    
    if axis == 0:
        posY = [pm.PyNode(p).getPosition(space=space)[1] for p in vtxList]
        posZ = [pm.PyNode(p).getPosition(space=space)[2] for p in vtxList]
        cenYZ = [(max(posY) + min(posY))/2, (max(posZ) + min(posZ))/2]
        length = [sqrt(pow(y-cenYZ[0],2) + pow(z-cenYZ[1],2)) for (y,z) in zip(posY,posZ)]
        
        if mode==0:
            r=min(length)
        if mode==1:
            r = (max(length) + min(length))/2
        if mode==2:
            r = max(length)
            
        sinCos = [[(y-cenYZ[0])/l,(z-cenYZ[1])/l] for (y,z,l) in zip(posY,posZ,length)]
        for (vtx,rad) in zip(vtxList,sinCos):
            valueY = cenYZ[0] + r*rad[0]
            valueZ = cenYZ[1] + r*rad[1] 
            if space=='object':
                pm.move(valueY,vtx,moveY=True,objectSpace=True)
                pm.move(valueZ,vtx,moveZ=True,objectSpace=True)
            else:
                pm.move(valueY,vtx,moveY=True)
                pm.move(valueZ,vtx,moveZ=True)

    if axis == 1:
        posX = [pm.PyNode(p).getPosition(space=space)[0] for p in vtxList]
        posZ = [pm.PyNode(p).getPosition(space=space)[2] for p in vtxList]
        cenXZ = [(max(posX) + min(posX))/2, (max(posZ) + min(posZ))/2]
        length = [sqrt(pow(x-cenXZ[0],2) + pow(z-cenXZ[1],2)) for (x,z) in zip(posX,posZ)]
        
        if mode==0:
            r=min(length)
        if mode==1:
            r = (max(length) + min(length))/2
        if mode==2:
            r = max(length)
            
        sinCos = [[(x-cenXZ[0])/l,(z-cenXZ[1])/l] for (x,z,l) in zip(posX,posZ,length)]
        for (vtx,rad) in zip(vtxList,sinCos):
            valueX = cenXZ[0] + r*rad[0]
            valueZ = cenXZ[1] + r*rad[1] 
            if space=='object':
                pm.move(valueX,vtx,moveX=True,objectSpace=True)
                pm.move(valueZ,vtx,moveZ=True,objectSpace=True)
            else:
                pm.move(valueX,vtx,moveX=True)
                pm.move(valueZ,vtx,moveZ=True)

    if axis == 2:
        posX = [pm.PyNode(p).getPosition(space=space)[0] for p in vtxList]
        posY = [pm.PyNode(p).getPosition(space=space)[1] for p in vtxList]
        cenXY = [(max(posX) + min(posX))/2, (max(posY) + min(posY))/2]
        length = [sqrt(pow(x-cenXY[0],2) + pow(y-cenXY[1],2)) for (x,y) in zip(posX,posY)]
        
        if mode==0:
            r=min(length)
        if mode==1:
            r = (max(length) + min(length))/2
        if mode==2:
            r = max(length)
            
        sinCos = [[(x-cenXY[0])/l,(y-cenXY[1])/l] for (x,y,l) in zip(posX,posY,length)]
        for (vtx,rad) in zip(vtxList,sinCos):
            valueX = cenXY[0] + r*rad[0]
            valueY = cenXY[1] + r*rad[1] 
            if space=='object':
                pm.move(valueX,vtx,moveX=True,objectSpace=True)
                pm.move(valueY,vtx,moveY=True,objectSpace=True)
            else:
                pm.move(valueX,vtx,moveX=True)
                pm.move(valueY,vtx,moveY=True)
                
class GUI:
    windowName='AlignVertexOnCircle'
    _checkBox=None
    
    def __init__(self):
        if pm.window(self.windowName, exists=True):
            pm.deleteUI(self.windowName)
            
    def callBack(self,*args):
        axisName = pm.radioCollection(self.rc1, q=True, select=True)
        if axisName == 'X':
            axis=0
        if axisName == 'Y':
            axis=1
        if axisName == 'Z':
            axis=2
            
        modeName = pm.radioCollection(self.rc2, q=True, select=True)
        if modeName == 'Min':
            mode=0
        if modeName == 'Cen':
            mode=1
        if modeName == 'Max':
            mode=2
            
        AlignVertexOnCircle(axis,mode,self.checkBox.getValue())
        
        
    def show(self):
        window = pm.window(self.windowName,title=self.windowName)
        with window:
            with pm.frameLayout(bs='in',label=u'頂点を円上に整列'):
                with pm.frameLayout(bs='in', label=u'射影平面'):
                    self.rc1 = pm.radioCollection()
                    with pm.rowLayout(numberOfColumns=3):
                        pm.radioButton('X', label=u'YZ', select=True)
                        pm.radioButton('Y', label=u'XZ')
                        pm.radioButton('Z', label=u'XY')
                with pm.frameLayout(bs='in', label=u'円の半径'):
                    self.rc2 = pm.radioCollection()
                    with pm.rowLayout(numberOfColumns=3):
                        pm.radioButton('Min', label=u'最短値', select=True)
                        pm.radioButton('Cen', label=u'中間値')
                        pm.radioButton('Max', label=u'最長値')
                        self.checkBox = pm.checkBox(label = u'ワールド軸 (off　/　ローカル)', value=True)
                        pm.button(label='Submit',width=40,height=32,command=pm.Callback(self.callBack))

def main():
    w=GUI()
    w.show()

main()
