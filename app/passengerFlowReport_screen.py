import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen

qtCreatorFile = "ui/passengerFlowReport.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class PassengerFlowReportFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.resetButton.clicked.connect(self.ResetFilter)
		self.CreateView(startTime,endTime)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.resetButton.clicked.connect(self.ResetFilter)
		self.CreateView(startTime,endTime)
	def CreateView(self, startTime, endTime):
		startTime = self.startDateTimeEdit.dateTime().toPyDateTime()
		endTime = self.endDateTimeEdit.dateTime().toPyDateTime()	
		data = backend.PassengerFlowReport(startTime,endTime)

		if type(data) != list:
			self.error = "Unkown Error\n" + str(data)
			self.OpenError()
			return

		self.tableWidget.setRowCount = len(data)
		font = QtGui.QFont()
		font.setBold(True)
		for i in range(0,len(data)):
			self.tableWidget.insertRow(i)
			suspended = False;
			if data[i][2] == "Suspended":
				suspended = True
			for j in range(0,self.tableWidget.columnCount()):
				if j == 0:
					cardNum = str(data[i][j])
					cardNum = cardNum[0:4] + " " + cardNum[4:8] + " " + cardNum[8:12] + " " + cardNum[12:16] 
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(cardNum))
				elif j == 1:
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem("$"+"{0:.2f}".format(data[i][j])))
				else:
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(data[i][j]))
				if suspended:
					self.tableWidget.item(i,j).setFont(font)
		self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.Stretch)
		self.tableWidget.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.Stretch)
		self.tableWidget.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.Stretch)
	def UpdateFilter(self): 
		startTime = self.startDateTimeEdit.dateTime().toPyDateTime()
		endTime = self.endDateTimeEdit.dateTime().toPyDateTime()
		self.hide()
		self.createView(startTime,endTime)
		self.success = "Updated View!"
		self.show()
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