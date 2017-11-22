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
		self.CreateModel()
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createNewStationButton.clicked.connect(self.OpenCreateNewStation)
		self.viewStationButton.clicked.connect(self.ViewStation)
		self.CreateModel()
	def OpenCreateNewStation(self): 
		self.frame = createNewStation_screen.CreateNewStationFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
	def CreateModel(self):
		data = [[1,2,3,4],[5,6,7,8]]
		self.tableWidget.setRowCount = len(data)
		self.tableWidget.sortingEnabled = False
		for i in range(0,len(data)):
			rowInd = i
			self.tableWidget.insertRow(i)
			for j in range(0,self.tableWidget.columnCount()):
				self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(data[i][j])))
		self.tableWidget.sortingEnabled = True
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
	stationListingWindow = StationListingFrame()
	stationListingWindow.show()
	sys.exit(app.exec_())