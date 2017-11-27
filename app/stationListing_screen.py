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
		self.updateViewButton.clicked.connect(self.UpdateView)
		self.CreateView()
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createNewStationButton.clicked.connect(self.OpenCreateNewStation)
		self.viewStationButton.clicked.connect(self.ViewStation)
		self.updateViewButton.clicked.connect(self.UpdateView)
		self.CreateView()
	def OpenCreateNewStation(self): 
		self.frame = createNewStation_screen.CreateNewStationFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
	def UpdateView(self): 
		self.hide()
		while (self.tableWidget.rowCount() > 0):
			self.tableWidget.removeRow(0)
		self.CreateView()
		self.success = "Updated View!"
		self.show()
		self.OpenSuccess()
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
			self.error = "No Station Selected"
			self.OpenError()
			return

		#Get a list of pointers to all the selected Items (all items in the row) 
		#& use the first one arbitrarily to get the row index
		row = self.tableWidget.selectedItems()[0].row()

		#Get the StopID of the selected Station for backend
		stopId = self.tableWidget.item(row,1).data(0) #stopId is in the index=1 column
		data = backend.ViewSingleStation(stopId)
		data_dict = {}
		data_dict["Station Name"] = data[0]
		data_dict["Stop ID"] = data[1]
		data_dict["Entry Fare"] = data[2]
		data_dict["Status"] = not data[3]
		if (data[4]):
			#if isTrain:
			data_dict["Nearest Intersection"] = "Not Available for Trains"
		else:
			if (backend.ViewIntersection(data_dict["Stop ID"]) == None):
				data_dict["Nearest Intersection"] = "Null"
			else: 
				data_dict["Nearest Intersection"] = backend.ViewIntersection(data_dict["Stop ID"])
		self.OpenStationDetail(data_dict)
	def OpenStationDetail(self, data_dict): 
		self.frame = stationDetail_screen.StationDetailFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		stationName = data_dict["Station Name"]
		stopId = data_dict["Stop ID"]
		fare = data_dict["Entry Fare"]
		isOpen = data_dict["Status"]
		nearestIntersection = data_dict["Nearest Intersection"]
		self.frame.UpdateValues(stationName,stopId,fare,isOpen,nearestIntersection)
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