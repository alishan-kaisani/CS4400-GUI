import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

#File loads up GUI Frame described below - connects all buttons and clicks & ties functions to backend

qtCreatorFile = "ui/error.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ErrorFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.closeButton.clicked.connect(self.CloseWindow)
		self.text = ""
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.closeButton.clicked.connect(self.CloseWindow)
		self.text = ""
	def CloseWindow(self): 
		self.close()
	def UpdateText(self):
		self.issueLabel.setText(self.text)


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = ErrorFrame()
	window.show()
	sys.exit(app.exec_())