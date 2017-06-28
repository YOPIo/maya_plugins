def getMeshList(Node, MeshList):
    MeshList.append(Node)
    children = Node.getChildren()   
    for i in children:     
        if i.numChildren()>0:
            getMeshList(i, MeshList)
        else:
            MeshList.append(i)
    return MeshList
 
sel = pm.selected()
MeshList = []  
 
for i in sel:
 tempList=[]
 l = getMeshList(i, tempList)
 for j in l:
  j.rename(j + '_Joint')
 MeshList.append(l)
 print MeshList