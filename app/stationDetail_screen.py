import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen
import backend

qtCreatorFile = "ui/stationDetail.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class StationDetailFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateStationButton.clicked.connect(self.UpdateStation)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateStationButton.clicked.connect(self.UpdateStation)
	def UpdateValues(self, stationName,stopId,fare,isOpen, nearestIntersection): 
		"""Fill in values for the specified station when coming in from station Listing page"""
		self.stationNameLabel.setText(stationName)
		self.stopIdLabel.setText(stopId)
		self.entryFareSpinBox.setValue(fare)
		self.openStationBox.setChecked(isOpen)
		self.nearestIntersectionTextLabel.setText(nearestIntersection)
	def UpdateStation(self):
		stopId = str(self.stopIdLabel.text())
		fare = self.entryFareSpinBox.value()
		status = not self.openStationBox.isChecked()
		#DB tracks isClosed not isOpen so passing on isClosed
		
		res = -1
		res = backend.ChangeStation(stopId,status,fare)

		if res == 1: 
			self.success = "Station updated!\n***Update StationListing view to see changes***"
			self.OpenSuccess()
		elif res == -1:
			self.error = "Error in Station update"
			self.OpenError()
			return
		else:
			self.error = "Unkown Error:\n" + str(res)
			self.OpenError()
	def OpenError(self):
		self.newframe = error_screen.ErrorFrame()
		self.newframe.InitFromOtherFile(Ui_Frame)
		self.newframe.text = self.error
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
	window = StationDetailFrame()
	window.show()
	sys.exit(app.exec_())