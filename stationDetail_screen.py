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
	def UpdateValues(self, stationName,stopId,fare,isOpen): 
		self.stationNameLabel.setText(stationName)
		self.stopIdLabel.setText(stopId)
		self.entryFareSpinBox.setValue(fare)
		self.openStationBox.setChecked(isOpen)
		#self.error = "Update Fare Function Not defined yet"
		#self.OpenError()
	def UpdateStation(self):
		self.error = "Update Station Function Not defined yet"
		self.OpenError()
	def OpenError(self):
		self.frame = error_screen.ErrorFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.text = self.error
		self.frame.UpdateText()
		self.frame.show()
	def OpenSuccess(self):
		self.frame = success_screen.SuccessFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.text = self.success;
		self.UpdateText()
		self.frame.show()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = StationDetailFrame()
	window.show()
	sys.exit(app.exec_())