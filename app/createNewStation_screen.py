import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import stationListing_screen
import error_screen
import success_screen
import time;
import backend

qtCreatorFile = "ui/createNewStation.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CreateNewStationFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createStationButton.clicked.connect(self.CreateStation)
		self.busStationButton.toggled.connect(self.BusButtonClicked)
		self.trainStationButton.toggled.connect(self.TrainButtonClicked)
	def BusButtonClicked(self,enabled):
		if enabled:
			self.nearestIntersectionTextEdit.setEnabled(True)
	def TrainButtonClicked(self,enabled):
		if enabled:
			self.nearestIntersectionTextEdit.setEnabled(False)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createStationButton.clicked.connect(self.CreateStation)
		self.busStationButton.toggled.connect(self.BusButtonClicked)
		self.trainStationButton.toggled.connect(self.TrainButtonClicked)
	def CreateStation(self): 
		stationName = str(self.stationNameTextEdit.text())
		stopId = str(self.stopIdTextEdit.text())
		entryFare = self.entryFareSpinBox.value
		busStation = self.busStationButton.isChecked()
		trainStation = self.trainStationButton.isChecked()
		openStation = self.openStationBox.isChecked()
		self.error = "Create new station function not defined yet"
		self.OpenStationListing()
		self.OpenError()
	def OpenStationListing(self):
		self.frame = stationListing_screen.StationListingFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
	def OpenError(self):
		self.newframe = error_screen.ErrorFrame()
		self.newframe.InitFromOtherFile(Ui_Frame)
		self.newframe.text = self.error;
		self.newframe.UpdateText()
		self.newframe.show()
	def OpenSuccess(self):
		self.newframe = success_screen.SuccessFrame()
		self.newframe.InitFromOtherFile(Ui_Frame)
		self.newframe.text = self.success;
		self.newframe.UpdateText()
		self.newframe.show()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = CreateNewStationFrame()
	window.show()
	sys.exit(app.exec_())