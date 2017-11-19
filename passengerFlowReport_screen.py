import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

qtCreatorFile = "ui/passengerFlowReport.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class PassengerFlowReportFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.resetButton.clicked.connect(self.ResetFilter)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.resetButton.clicked.connect(self.ResetFilter)
	def UpdateFilter(self): 
		print("Updating Filter...")
	def ResetFilter(self): 
		print("Reseting Filter...")

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = PassengerFlowReportFrame()
	window.show()
	sys.exit(app.exec_())