import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import backend
import fileinput

#File loads up GUI Frame described below - connects all buttons and clicks & ties functions to backend

qtCreatorFile = "ui/errorDialog.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ErrorDialogFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		#self.closeButton.clicked.connect(self.CloseWindow)
		self.newText = ""
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		#self.closeButton.clicked.connect(self.CloseWindow)
		self.oldText = ""
		self.newText = ""
	def CloseWindow(self): 
		self.hide()
	def UpdateText(self):
		writeToFile(self.newText)
		print("updating dialog text...")


def writeToFile(newText):
	with open("ui/errorDialog.ui", "r") as f: 
		data = f.readlines()
		new_line = "<string>" + newText + "</string>\n"
		data[50-1] = new_line #I know the text I want to edit is always going to be sitting at line 50

	with open("ui/errorDialog.ui", 'w') as f: 
		f.writelines(data)

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = LoginFrame()
	window.show()
	sys.exit(app.exec_())