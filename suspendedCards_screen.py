import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

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
		print("Transfering to new Owner...")
	def TransferPrevOwner(self): 
		print("Transfering to prev Owner...")


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = SuspendedCardsFrame()
	window.show()
	sys.exit(app.exec_())