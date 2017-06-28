# -*- coding: utf-8

import os
import sys
import maya.cmds as cmds


# パスをファイルの場所にあわせて設定してください
PATH = "/Users/xxx/maya/"


# パスの追加
sys.path.append(PATH)
sys.path.append(PATH + "ChangedCommand.py")
sys.path.append(PATH + "ConnectHairSystems.py")
sys.path.append(PATH + "HairSystem.py")
'''
パスを削除する場合は以下を実行
sys.path.remove(PATH)
sys.path.remove(PATH + "ChangedCommand.py")
sys.path.remove(PAHT + "ConnectHairSystems.py")
sys.path.remove(PATH + "HairSystem.py")
'''

# 必要なモジュールのインポート		
import ChangedCommand
import ConnectHairSystem

class CreateUI:

	def intiUI(self):
		# intSliderの最大値の設定 default値 -> 10
		cmds.intSlider("intSlider", edit = True, maxValue = 10)
		cmds.textScrollList("scrollList", edit = True, enable = False)

	def loadUI(self):

		self.path = PATH + 'HairSystemTool.ui'
		self.dialog = cmds.loadUI(uiFile = self.path)
		self.window = cmds.showWindow(self.dialog)
		self.intiUI()


def main():

	if cmds.window("HairSystemTool", ex = True):
		cmds.deleteUI("HairSystemTool")


	ui = CreateUI()
	ui.loadUI()


if __name__ == '__main__':
	main()