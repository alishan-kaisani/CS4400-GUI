import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen
import backend

qtCreatorFile = "ui/tripHistory.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class TripHistoryFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.Update)
		self.resetButton.clicked.connect(self.Reset)
		startTime = self.startDateTimeEdit.dateTime().toPyDateTime()
		endTime = self.endDateTimeEdit.dateTime().toPyDateTime()
		self.CreateView(startTime,endTime)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.Update)
		self.resetButton.clicked.connect(self.Reset)
		startTime = self.startDateTimeEdit.dateTime().toPyDateTime()
		endTime = self.endDateTimeEdit.dateTime().toPyDateTime()
		self.CreateView(startTime,endTime)
	def Update(self): 
		startTime = self.startDateTimeEdit.dateTime().toPyDateTime()
		endTime = self.endDateTimeEdit.dateTime().toPyDateTime()
		self.hide()
		while (self.tableWidget.rowCount() > 0):
			self.tableWidget.removeRow(0)
		self.CreateView(startTime,endTime)
		self.success = "Updated View!"
		self.show()
		self.OpenSuccess()
	def CreateView(self, startTime, endTime):
		self.tableWidget.setSortingEnabled(False)
		data = backend.TripHistoryOfUser(startTime,endTime)
		self.tableWidget.setRowCount = len(data)
		for i in range(0,len(data)):
			self.tableWidget.insertRow(i)
			if (data[i][1]) != None:
				start_name = str(backend.ViewSingleStation(data[i][1])[0]) #get data from start_stopId
			else:
				start_name = "NULL"
			if (data[i][2]) != None:
				end_name = str(backend.ViewSingleStation(data[i][2])[0]) #get data from end_stopId
			else:
				end_name = "NULL"
			data[i] = [data[i][0], start_name, end_name, ("$"+"{:0.2f}".format(data[i][3])), (data[i][4])[0:4]]
			#entry 1: replace breezecardnum with first 4 digits
			#entry 2: replace start_stopId with start_name
			#entry 3: repalce end_stopId with end_name
			#entry 4: replace fare with nicely formatted string
			for j in range(0,self.tableWidget.columnCount()):
				self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(data[i][j]))
		
		#formatting
		self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(3,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(3,QtWidgets.QHeaderView.Stretch)
		self.tableWidget.setSortingEnabled(True)
	def Reset(self): 
		#year,month,day,hour,min
		start = QtCore.QDateTime(1900,1,1,12,0)
		end = QtCore.QDateTime(2100,12,31,12,0)
		self.startDateTimeEdit.setDateTime(start)
		self.endDateTimeEdit.setDateTime(end)
	def OpenError(self):
		self.newframe = error_screen.ErrorFrame()
		self.newframe.InitFromOtherFile(Ui_Frame)
		self.newframe.text = self.error
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
	window = TripHistoryFrame()
	window.show()
	sys.exit(app.exec_())