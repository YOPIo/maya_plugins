import pymel.core as pm

def getLeafNode(node,name,num):
    if node.numChildren() is 1:
        pm.rename(node, name + str(num))
        num += 1
        node = getLeafNode(node.getChildren()[0],name,num)
    else:
        pm.rename(node, name + str(num))
    return node
    
def setChildrentoParent(node):
    for i in [i for i in node.getChildren() if i.type() == 'transform']:
        node.getParent().addChild(i)

#-----assign new hair system to curve
#-----input (inputCurve, baseName)            
#-----return [inputCurve, hairSystem, Follicle, outputCurve]
    
def assignNewHairSystem(inputCV,baseName):
    pm.select(inputCV)
    pm.mel.assignNewHairSystem()
    hs = pm.PyNode(u'hairSystem1')
    fo = pm.PyNode(u'follicle1')
    icv = fo.getChildren()[1]
    cv = pm.PyNode(u'curve1')
    fop = fo.getParent()
    cvp = cv.getParent()
    hs.startCurveAttract.set(.5)
    pm.rename(hs, baseName + u'_hairSystem')
    pm.rename(fo, baseName + u'_follicle')
    pm.rename(cv, baseName + u'_outputCurve')
    pm.group(hs,fo,cv, name = baseName + '_hairSystemGroup')
    setChildrentoParent(fo)
    pm.delete(fop,cvp)
    
    print hs
    
    return [icv,hs,fo,cv]
    
def assignHairSystem(inputCV, baseName, hairSystem):
    pm.select(inputCV)
    print hairSystem
    pm.mel.eval('assignHairSystem ' + hairSystem)
    fo = pm.PyNode(u'follicle1')
    icv = fo.getChildren()[1]
    cv = pm.PyNode(u'curve1')
    fop = fo.getParent()
    cvp = cv.getParent()
    pm.rename(fo, baseName + u'_follicle')
    pm.rename(cv, baseName + u'_outputCurve')
    pm.group(fo, cv, name = baseName + '_hairSystemGroup')
    setChildrentoParent(fo)
    pm.delete(fop,cvp)
    
    return [icv,hairSystem,fo,cv]
    
def setCurveController(inputCurve, baseName):
    #print pm.getAttr(inputCurve + u'Shape.controlPoint')
    CVContGP = pm.group(empty = True,name = baseName + u'_curveControllerGroup')
    for i in range(0,inputCurve.spans.get() + pm.getAttr(inputCurve + '.degree')):
        locator = pm.spaceLocator(name = baseName + u'_curveController' + str(i+1))
        pm.PyNode(inputCurve + u'Shape').controlPoints[i] >> locator.translate
        pm.PyNode(inputCurve + u'Shape').controlPoints[i] // locator.translate
        locator.translate >> pm.PyNode(inputCurve + u'Shape').controlPoints[i]
        CVContGP.addChild(locator)
    return CVContGP
        
def setParentConstraint(targetNode, nodeList, baseName):
    pc =  pm.parentConstraint(targetNode,nodeList,maintainOffset = True, weight = .1)
    return pc
    
def setDecomposeMatrix(curveContGP, inputCurve, baseName):
    i = 1
    for cv in sorted([cv for cv in curveContGP.getChildren() if cv.type() == 'transform']):
        dm = pm.shadingNode('decomposeMatrix', asUtility = True, name = baseName + '_decomposeMatrix' + str(i))
        cv.worldMatrix >> dm.inputMatrix
        dm.outputTranslate >> inputCurve.controlPoints[i-1]
        i += 1
        insertParentGroupwithAttr(cv)
        
def insertParentGroupwithAttr(node):
    nodeGP = pm.group(node, name = node.name() + '_attr')
    nodeGP.setTranslation(node.getTranslation())
    node.setTranslation([0,0,0])

def listNodes():
    temp = pm.selected()
    pm.select(all = True, hierarchy = True)
    hairSystems = pm.selected(type = 'hairSystem')
    print hairSystems
    pm.select(temp)
    return hairSystems

def main(targetJointNum, attachNewHairSystemFlag, hairSystemName):

    #-----Load plugins
    if pm.pluginInfo('matrixNodes.mll', query = True, loaded = True):
        print 'matrixNodes.mll is loaded'
    else:
        pm.loadPlugin('matrixNodes.mll')

    rootNode =  pm.selected()[:targetJointNum]
    print rootNode
    if not hairSystemName == '':
        hairSys = pm.PyNode(hairSystemName)
    for i in pm.selected()[targetJointNum:]:
        if i.type() == 'joint':
            pm.parent(i, world = True)
            baseName = i.name()
            leafJoint = getLeafNode(i, baseName + u'_joint',1)
            if i is not leafJoint:
                Handle = pm.ikHandle(startJoint= i,endEffector = leafJoint, solver = 'ikSplineSolver')
                pm.rename(Handle[0], baseName + u'_ikHandle')
                pm.rename(Handle[1], baseName + u'_effector')
                pm.rename(Handle[2], baseName + u'_ikControlCurve')
                inputCV = pm.duplicate(Handle[2], name = baseName + u'_inputCurve')
                if attachNewHairSystemFlag == 1:
                    afterANHS = assignNewHairSystem(inputCV,baseName)
                    attachNewHairSystemFlag = 0
                    print 'yahoo!'
                else:
                    print 'google!'
                    afterANHS = assignHairSystem(inputCV,baseName,hairSys)
                hairSys = afterANHS[1]
                pm.PyNode(afterANHS[3] + u'Shape').worldSpace >> pm.PyNode(Handle[2] + u'Shape').create
                #print pm.listAttr(pm.PyNode(afterANHS[3] + u'Shape'))
                #print pm.listAttr(pm.PyNode(Handle[2] + u'Shape'))
                #print afterANHS
                curveContGroup = setCurveController(afterANHS[0],baseName)
                setParentConstraint(rootNode, curveContGroup, baseName)
                setDecomposeMatrix(curveContGroup,afterANHS[0],baseName)
                i.setParent(curveContGroup)
                pm.group(Handle[0], Handle[2],name = baseName + '_ikHandleGroup')

        else:
            print i + 'is not joint'

main(1,1,'')