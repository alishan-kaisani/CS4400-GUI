import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

qtCreatorFile = "ui/manageCards.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ManageCardsFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.addCardButton.clicked.connect(self.AddCard)
		self.addValueButton.clicked.connect(self.AddValue)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.addCardButton.clicked.connect(self.AddCard)
		self.addValueButton.clicked.connect(self.AddValue)
	def AddCard(self): 
		print("Adding Card...")
	def AddValue(self): 
		print("Adding Value...")

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = ManageCardsFrame()
	window.show()
	sys.exit(app.exec_())