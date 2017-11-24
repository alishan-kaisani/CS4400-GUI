import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen

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
		self.stationNameLabel.setText(stationName)
		self.stopIdLabel.setText(stopId)
		self.entryFareSpinBox.setValue(fare)
		self.openStationBox.setChecked(isOpen)
		self.nearestIntersectionTextLabel.setText(nearestIntersection)
		#self.error = "Update Fare Function Not defined yet"
		#self.OpenError()
	def UpdateStation(self):
		self.error = "Update Station Function Not defined yet"
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