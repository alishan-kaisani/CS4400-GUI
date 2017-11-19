import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

qtCreatorFile = "ui/tripHistory.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class TripHistoryFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.Update)
		self.resetButton.clicked.connect(self.Reset)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.Update)
		self.resetButton.clicked.connect(self.Reset)
	def Update(self): 
		print("Updating Filter...")
	def Reset(self): 
		print("Resetting Filter...")

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = TripHistoryFrame()
	window.show()
	sys.exit(app.exec_())