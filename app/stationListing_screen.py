import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import createNewStation_screen
import stationDetail_screen
import error_screen
import success_screen
import backend

qtCreatorFile = "ui/stationListing.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class StationListingFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createNewStationButton.clicked.connect(self.OpenCreateNewStation)
		self.viewStationButton.clicked.connect(self.ViewStation)
		self.CreateView()
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createNewStationButton.clicked.connect(self.OpenCreateNewStation)
		self.viewStationButton.clicked.connect(self.ViewStation)
		self.CreateView()
	def OpenCreateNewStation(self): 
		self.frame = createNewStation_screen.CreateNewStationFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
	def CreateView(self):
		data = backend.PrettifyViewStations()
		self.tableWidget.setRowCount = len(data)
		font = QtGui.QFont()
		font.setBold(True)
		for i in range(0,len(data)):
			self.tableWidget.insertRow(i)
			closed = False;
			if data[i][3] == "Closed":
				closed = True;
			for j in range(0,self.tableWidget.columnCount()):
				if j != 2:
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(data[i][j])))
				else:
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem("$"+"{0:.2f}".format(data[i][j])))
				if closed:
					self.tableWidget.item(i,j).setFont(font)
		self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeToContents)
	def ViewStation(self):
		# cur_stopId = cur_station.data("Stop Id")
		if (len(self.tableWidget.selectedItems()) == 0):
			self.error = "No Station Selcted"
			self.OpenError()
			return

		#Get a list of pointers to all the selected Items (all items in the row) 
		#& use the first one arbitrarily to get the row index
		row = self.tableWidget.selectedItems()[0].row()

		#Get the StopID of the selected Station for backend
		self.tableWidget.item(row,1)
		

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