import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import backend
import error_screen
import success_screen

qtCreatorFile = "ui/breezeCardManagement.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class BreezeCardManagementFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.resetButton.clicked.connect(self.ResetFilter)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.setValueButton.clicked.connect(self.SetValue)
		self.transferCardButton.clicked.connect(self.TransferCard)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.resetButton.clicked.connect(self.ResetFilter)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.setValueButton.clicked.connect(self.SetValue)
		self.transferCardButton.clicked.connect(self.TransferCard)
	def OpenError(self):
		self.frame = error_screen.ErrorFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.text = self.error
		self.frame.UpdateText()
		self.frame.show()
	def OpenSuccess(self):
		self.frame = success_screen.SuccessFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.text = self.success
		self.frame.UpdateText()
		self.frame.show()
	def ResetFilter(self): 
		self.ownerTextEdit.setText("")
		self.cardNumberTextEdit.setText("")
		self.money1SpinBox.setValue(0.00)
		self.money2SpinBox.setValue(1000.00)
		self.checkBox.setChecked(False)
	def UpdateFilter(self): 
		self.error = "Update Filter Function Not Defined Yet"
		self.OpenError()
	def SetValue(self): 
		self.error = "Set Card Value Function Not Defined Yet"
		self.OpenError()
	def TransferCard(self): 
		self.error = "Transfer Card Function Not Defined Yet"
		self.OpenError()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = BreezeCardManagementFrame()
	window.show()
	sys.exit(app.exec_())