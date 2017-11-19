import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import createNewStation_screen
import stationDetail_screen

qtCreatorFile = "ui/stationListing.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class StationListingFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createNewStationButton.clicked.connect(self.OpenCreateNewStation)
		self.viewStationButton.clicked.connect(self.OpenStationDetail)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createNewStationButton.clicked.connect(self.OpenCreateNewStation)
		self.viewStationButton.clicked.connect(self.OpenStationDetail)
	def OpenCreateNewStation(self): 
		self.frame = createNewStation_screen.CreateNewStationFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
		print("opening new station page...")
	def OpenStationDetail(self): 
		self.frame = stationDetail_screen.StationDetailFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		print("opening current station view...")


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	stationListingWindow = StationListingFrame()
	stationListingWindow.show()
	sys.exit(app.exec_())