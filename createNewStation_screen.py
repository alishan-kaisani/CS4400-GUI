import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import stationListing_screen

qtCreatorFile = "ui/createNewStation.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CreateNewStationFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createStationButton.clicked.connect(self.CreateStation)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createStationButton.clicked.connect(self.CreateStation)
	def CreateStation(self): 
		stationName = self.stationNameTextEdit.toPlainText()
		stopId = self.stopIdTextEdit.toPlainText()
		entryFare = self.entryFareTextEdit.toPlainText()
		busStation = self.busStationButton.isChecked()
		trainStation = self.trainStationButton.isChecked()
		openStation = self.openStationBox.isChecked()
		print("creating new station...")
		self.OpenStationListing()
	def OpenStationListing(self):
		self.frame = stationListing_screen.StationListingFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		print("opening station listing...")
		self.frame.show()
		self.hide()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = CreateNewStationFrame()
	window.show()
	sys.exit(app.exec_())