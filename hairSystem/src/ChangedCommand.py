# -*- coding: utf-8
import maya.cmds as cmds
import ConnectHairSystem

# lineEditの値が変更され、適切な値かチェックをする。適切な値の場合には値を更新し、sliderに反映させる。
def fromLineEdit2Slider(textFieldName, sliderName):

	# debug
	print("debug : Line 2 Slider")

	# lineEditからSliderに値を送る
	text = cmds.textField(textFieldName, query = True, text = True)

	# intSliderの最大値を得る
	maxVal = cmds.intSlider(sliderName, query = True, maxValue = True)
	print maxVal

	if text.isdigit():

		try:
			value = int(text)	

		except UnboundLocalError, ue:
			print u"stringはダメ"

		# stringが入力された場合に実行
		except ValueError, e:
			print u"stringはダメ"

	# textFieldに入力された値がmaxValよりも大きかった場合にはmaxValueの更新を行う
	if maxVal < value:
		cmds.intSlider(sliderName, edit = True, maxValue = value)
		print "max value " + str(maxVal) + " was overrided."

	# sliderにtextEditの値を反映させる
	cmds.intSlider(sliderName, edit = True, value = value)


# スライダの値をlineEditに反映させる。
def fromSlider2LineEdit(textFieldName, sliderName):

	# debug
	print "slider : " + str(cmds.intSlider(sliderName, query = True, value = True))

	# SliderからlineEditに値を送る(存在するはず)
	slider = cmds.intSlider(sliderName, query =  True, value = True)
	cmds.textField(textFieldName , edit = True, text = str(slider))


# textScrollListの表示をやめて、新しくHair Systemを作成するようにする
def changeRadio2CreateMode(scrollListName):

	cmds.textScrollList(scrollListName, edit = True, da = True)
	
	# textScrollListを使用できないようにする
	cmds.textScrollList(scrollListName, edit = True, enable = False)
	

# textScrollListの表示を行うようにする。
def changeRadio2AttachMode(scrollListName):

	# textScrollListを使用できるようにする
	cmds.textScrollList(scrollListName, edit = True, enable = True)

	# textScrollListの項目を全て削除する
	cmds.textScrollList(scrollListName, edit = True, ra= True)

	# ConnectHairSystemからリストを持ってきて表示する
	reload(ConnectHairSystem)
	hairList = ConnectHairSystem.listNodes()

	# textScrollListにhairSystemを加える
	for t in hairList:
		print t
		cmds.textScrollList(scrollListName, edit = True, a = t.name())

	cmds.select()


# Create ModeまたはAttach Modeに応じてコマンドを実行する
def doApplyCmd(scrollListName, intSliderName):

	# ラジオボタンが選択されているか
	hairFlag = cmds.radioButton("createRadioButton", query = True, select = True)
	targetJointNum = cmds.intSlider(intSliderName, query = True, value = True)

	# hairSystemを新たに作成
	if hairFlag:
		ConnectHairSystem.main(targetJointNum, 1, '')

	# hairSystemにアタッチ
	else:
		hairNodeName = cmds.textScrollList(scrollListName, query = True, selectItem = True)
		ConnectHairSystem.main(targetJointNum, 0, hairNodeName[0])



def doRefreshCmd(scrollListName):

	#debug
	print("refresh")
	changeRadio2AttachMode(scrollListName)

	if cmds.radioButton("createRadioButton", query = True, select = True):
		cmds.textScrollList(scrollListName, edit = True, enable = False)

	# qtで作成したuiファイルのQLineEditにアクセスする
	# openedField = cmds.fileDialog2(fm = 1, ds = 2)