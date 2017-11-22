import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import createNewStation_screen
import stationDetail_screen
import error_screen
import success_screen

qtCreatorFile = "ui/stationListing.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class StationListingFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createNewStationButton.clicked.connect(self.OpenCreateNewStation)
		self.viewStationButton.clicked.connect(self.ViewStation)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createNewStationButton.clicked.connect(self.OpenCreateNewStation)
		self.viewStationButton.clicked.connect(self.ViewStation)
	def OpenCreateNewStation(self): 
		self.frame = createNewStation_screen.CreateNewStationFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
	def ViewStation(self):
		self.error = "ViewStation Function not Defined Yet"
		self.OpenError()
	def OpenStationDetail(self): 
		self.frame = stationDetail_screen.StationDetailFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		stationName = "NAME"
		stopId = "STOPID"
		fare = 100.00
		isOpen = True
		self.frame.UpdateValues(stationName,stopId,fare,isOpen)
		self.frame.show()
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
	stationListingWindow = StationListingFrame()
	stationListingWindow.show()
	sys.exit(app.exec_())