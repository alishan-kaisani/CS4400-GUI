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
		self.returnStationButton.clicked.connect(self.OpenStationListing)
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
		self.returnStationButton.clicked.connect(self.OpenStationListing)
	def CreateStation(self): 
		#Read out data into vars
		stationName = str(self.stationNameTextEdit.text())
		stopId = str(self.stopIdTextEdit.text())
		entryFare = self.entryFareSpinBox.value()
		trainStation = self.trainStationButton.isChecked()
		isClosed = not self.openStationBox.isChecked()
		nearestIntersection = str(self.nearestIntersectionTextEdit.text())

		#Perform error handling
		if (stationName == "" or stopId == ''):
			self.error = "All fields must be filled"
			self.OpenError()
			return

		#entryFare will always have some sort of value in it

		if ((not (self.trainStationButton.isChecked())) and (not (self.busStationButton.isChecked()))):
			#Condition checks if neither radiobutton is checked
			self.error = "A staton must be assigned a type"
			self.OpenError()
			return

		#isClosed will always have a value

		res = -1
		res = backend.CreateStationWrapper(trainStation, stationName, stopId, entryFare, isClosed, nearestIntersection)
		if res == 1: 
			self.success = "Station created Successfully"
			self.OpenStationListing()
			self.OpenSuccess()
		elif res == -1:
			self.error = "Error in Station Creation"
			self.OpenError()
			return
		else:
			self.error = "Unknown Error:\n" + str(res)
			self.OpenError()
			return
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
		return
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