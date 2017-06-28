# coding:utf-8

import pymel.core as pm
import pymel.core.nodetypes as nt
import math
import sys, traceback

#-----3D Vector Class-----
class Vector_3D(object):
    def __init__(self, x=0.0, y=0.0, z=0.0, name=""):
        if isinstance(x,list):
            z=x[2]
            y=x[1]
            x=x[0]
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.name = str(name)

    def __add__(self,other):
        if isinstance(other,Vector_3D):
            return Vector_3D(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return Vector_3D(self.x + other, self.y + other, self.z + other)

    def __sub__(self,other):
        if isinstance(other,Vector_3D):
             return Vector_3D(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return Vector_3D(self.x - other, self.y - other, self.z - other)

    def __mul__(self,other):
        if isinstance(other,Vector_3D):
            return Vector_3D(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vector_3D(self.x * other, self.y * other, self.z * other)

    def __div__(self,other):
        if isinstance(other,Vector_3D):
            return Vector_3D(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vector_3D(self.x / other, self.y / other, self.z / other)

    def __str__(self):
        return "x = " + str(self.x) + ", y = " + str(self.y) + ", z = " + str(self.z)

    def inner(self,other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def outer(self,other):
        vec=Vector_3D()
        vec.x = self.y*other.z - self.z*other.y
        vec.y = self.z*other.x - self.x*other.z
        vec.z = self.x*other.y - self.y*other.x
        return vec

    def getNorm(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def getNormalizedVec(self):
        norm = self.getNorm()
        return self*(norm**(-1))

    def getInverseVec(self):
        return self*(-1)

    def getVectorElem(self):
        return [self.x, self.y, self.z]
    
#-----AlignHelper Class-----
class AlignHelper(object):
    @classmethod
    def getVector(cls,vtx):
        vec = Vector_3D(pm.xform(vtx,q=True,a=True,ws=True,t=True))
        vec.name = vtx
        return vec
    @classmethod
    def getVectors(cls,vtxList):
        vecs = []
        for vtx in vtxList:
            vecs.append(AlignHelper.getVector(vtx))
        return vecs
    @classmethod
    def moveVertex(cls,vector):
        pm.xform(vector.name, ws=True, a=True,t=vector.getVectorElem())

#-----GUI-----
class Align:
    windowName='Align Vertex on Plane'
    _checkBox=None

    a = Vector_3D()
    nv = Vector_3D()

    
    def __init__(self):
        if pm.window(self.windowName, exists=True):
            pm.deleteUI(self.windowName)

    def show(self):
        window = pm.window(self.windowName,title=self.windowName)
        window.setWidth(180)
        window.setHeight(240)
        
        with window:
            with pm.frameLayout(bs="in",label='Align Vertex'):
                pm.button(label='Get Normal Vector with selection',width=40,height=32,command=pm.Callback(self.GetNormalVector))
                pm.button(label='Align Vertex', width=40,height=32,command=pm.Callback(self.AlignVertex))

    def GetNormalVector(self):
        if not pm.selected():
            pm.warning("Select 3 vertexes")
            return
    
        pm.runtime.ConvertSelectionToVertices(pm.selected(flatten=True))
        vtxList = pm.filterExpand(selectionMask=31)
    
        if len(vtxList)<3:
            pm.warning("Select 3 vertexes")
            return

        self.a = AlignHelper.getVector(vtxList[0])
        b = AlignHelper.getVector(vtxList[1])
        c = AlignHelper.getVector(vtxList[2])
        ab = b-self.a
        ac = c-self.a
        self.nv = ab.outer(ac).getNormalizedVec()
        print self.nv
        print self.a
        
    def AlignVertex(self):
        print self.nv
        print self.a
        if not pm.selected():
            return
        pm.runtime.ConvertSelectionToVertices(pm.selected(flatten=True))
        vtxList = pm.filterExpand(selectionMask=31)
        
        vec = [v for v in AlignHelper.getVectors(vtxList)]
    
        for g in vec:
            moveVec = Vector_3D()
            ag = g - self.a
            moveVec = self.nv * (self.nv).inner(ag)
            moveVec = g - moveVec
            moveVec.name = g.name
            AlignHelper.moveVertex(moveVec)


def main():
    w=Align()
    w.show()
    
main()