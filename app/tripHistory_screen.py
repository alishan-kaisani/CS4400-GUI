import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen

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
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.Update)
		self.resetButton.clicked.connect(self.Reset)
		sstartTime = self.startDateTimeEdit.dateTime().toPyDateTime()
		endTime = self.endDateTimeEdit.dateTime().toPyDateTime()
	def Update(self): 
		startTime = self.startDateTimeEdit.dateTime().toPyDateTime()
		endTime = self.endDateTimeEdit.dateTime().toPyDateTime()
		self.hide()
		self.createView(startTime,endTime)
		self.success = "Updated View!"
		self.show()
		self.OpenSuccess()
	def CreateView(self, startTime, endTime):
		data = backend.ViewTripHistory(startTime,endTime)
		self.tableWidget.setRowCount = len(data)
		for i in range(0,len(data)):
			self.tableWidget.insertRow(i)
			for j in range(0,self.tableWidget.columnCount()):
				if j == 4: 
					#if dealing with breezecard #.. insert spaces
					cardNum = str(data[i][j])
					cardNum = str[0:4] + " " + str[4:8] + " " + str[8:12] + " " + str[12:16]
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(cardNum))
				elif j == 3:
					#if dealing with fare paid.. adjust formating 
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem("$"+"{0:.2f}".format(data[i][j])))
				else:
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(data[i][j]))
					self.tableWidget.item(i,j).setFont(font)
		self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(2,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(3,QtWidgets.QHeaderView.ResizeToContents)
	def Reset(self): 
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
	window = TripHistoryFrame()
	window.show()
	sys.exit(app.exec_())