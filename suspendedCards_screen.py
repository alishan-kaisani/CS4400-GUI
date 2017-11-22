import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen

qtCreatorFile = "ui/suspendedCards.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class SuspendedCardsFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.newOwnerButton.clicked.connect(self.TransferNewOwner)
		self.prevOwnerButton.clicked.connect(self.TransferPrevOwner)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.newOwnerButton.clicked.connect(self.TransferNewOwner)
		self.prevOwnerButton.clicked.connect(self.TransferPrevOwner)
	def TransferNewOwner(self): 
		self.error = "Transfer New Owner Function Not Defined yet"
		self.OpenError()
	def TransferPrevOwner(self): 
		self.error = "Transfer Prev Owner Function Not Defined yet"
		self.OpenError()
	def OpenError(self):
		self.frame = error_screen.ErrorFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.text = self.error
		self.frame.UpdateText()
		self.frame.show()
	def OpenSuccess(self):
		self.frame = success_screen.SuccessFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.text = self.success;
		self.UpdateText()
		self.frame.show()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = SuspendedCardsFrame()
	window.show()
	sys.exit(app.exec_())