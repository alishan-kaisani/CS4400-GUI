import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

qtCreatorFile = "ui/breezeCardManagement.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class BreezeCardManagementFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.resetButton.clicked.connect(self.ResetFilter)
		self.updateFilterButton.clicked.connect(self.UpdateFilter)
		self.setValueButton.clicked.connect(self.SetValue)
		self.transferCardButton.clicked.connect(self.TransferCard)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.resetButton.clicked.connect(self.ResetFilter)
		self.updateFilterButton.clicked.connect(self.UpdateFilter)
		self.setValueButton.clicked.connect(self.SetValue)
		self.transferCardButton.clicked.connect(self.TransferCard)
	def ResetFilter(self): 
		print("Reseting Filter...")
	def UpdateFilter(self): 
		print("Updating Filter...")
	def SetValue(self): 
		print("Setting Card Value...")
	def TransferCard(self): 
		print("Transfering card...")

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = BreezeCardManagementFrame()
	window.show()
	sys.exit(app.exec_())