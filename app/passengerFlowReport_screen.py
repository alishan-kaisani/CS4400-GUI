import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen
from datetime import datetime

qtCreatorFile = "ui/passengerFlowReport.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class PassengerFlowReportFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.resetButton.clicked.connect(self.ResetFilter)
		self.CreateView(datetime(2017,1,1,1,0,0,0),datetime(2017,12,31,11,59,0,0))
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.resetButton.clicked.connect(self.ResetFilter)
		self.CreateView(datetime(2017,1,1,1,0,0,0),datetime(2017,12,31,11,59,0,0))
	def CreateView(self, startTime, endTime):
		startTime = self.startDateTimeEdit.dateTime().toPyDateTime()
		endTime = self.endDateTimeEdit.dateTime().toPyDateTime()	

		if not (endTime > startTime):
			self.error = "Endtime must be greater than startTime"
			self.OpenError()
			return

		data = backend.ViewPassengerFlowReport(startTime,endTime)

		if type(data) != list:
			self.error = "Unkown Error\n" + str(data)
			self.OpenError()
			return

		self.tableWidget.setRowCount = len(data)
		for i in range(0,len(data)):
			self.tableWidget.insertRow(i)
			for j in range(0,self.tableWidget.columnCount()):
				if j == 4:
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem("$"+"{0:.2f}".format(data[i][j])))
				else:
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(data[i][j]))
		self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
		self.tableWidget.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
		self.tableWidget.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.Stretch)
		self.tableWidget.horizontalHeader().setSectionResizeMode(3,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(4,QtWidgets.QHeaderView.Stretch)
	def UpdateFilter(self): 
		startTime = self.startDateTimeEdit.dateTime().toPyDateTime()
		endTime = self.endDateTimeEdit.dateTime().toPyDateTime()
		self.hide()
		self.createView(startTime,endTime)
		self.show()
		self.success = "Updated View!"
		self.OpenSuccess()
	def ResetFilter(self): 
		#year,month,day,hour,min
		start = QtCore.QDateTime(2017,1,1,12,0)
		end = QtCore.QDateTime(2017,12,31,12,0)
		self.startDateTimeEdit.setDateTime(start)
		self.endDateTimeEdit.setDateTime(end)
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
	window = PassengerFlowReportFrame()
	window.show()
	sys.exit(app.exec_())