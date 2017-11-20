import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

qtCreatorFile = "ui/stationDetail.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class StationDetailFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateFareLabel.mousePressEvent = self.UpdateFare
		self.updateStationButton.clicked.connect(self.UpdateStation)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateFareLabel.mousePressEvent = self.UpdateFare
	def UpdateFare(self, event): 
		fare = self.fareTextEdit.toPlainText()
		print("updating fare...")
	def UpdateStation(self):
		print("updating station")


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = StationDetailFrame()
	window.show()
	sys.exit(app.exec_())