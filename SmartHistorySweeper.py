import pymel.core as pm
import sys

sys.dont_write_bytecode = True 

def SmartHistorySweeper():
    if not pm.selected():
        
        if SHS_HasDeformer():
            pm.runtime.BakeAllNonDefHistory()
        else:
            pm.runtime.DeleteAllHistory()

    else:
        if SHS_HasDeformer():
            pm.runtime.DeleteHistory()
        else:
            pm.runtime.BakeNonDefHistory()

def SHS_HasDeformer():

    deformers = pm.eval("getAllChains")

    if not deformers == None:
        return True

    else:
        return False

class SmartHistorySweeperGUI:
    windowsName = 'SmartHistorySweeper'
    _checkBox = None

    def __init__(self):
        if pm.window(self.windowName, exists = True):
            pm.deleteUI(self.windowName)

    def callBack(self,*args):
        SmartHistorySweeper()

    def show(self):
        window = pm.window(self.windowName, title = self.windowName)
        with window:
            with pm.frameLayout(bs='in', label=u'オブジェクトからヒストリーの削除'):
                pm.button(label='Submit',width=40,height=32,command=pm.Callback(self.callBack))
