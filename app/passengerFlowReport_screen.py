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
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.resetButton.clicked.connect(self.ResetFilter)
	def UpdateFilter(self): 
		self.error = "Update Filter Function not Defined Yet"
		self.OpenError()
	def ResetFilter(self): 
		#year,month,day,hour,min
		start = QtCore.QDateTime(2017,1,1,12,0)
		end = QtCore.QDateTime(2017,12,31,12,0)
		self.startDateTimeEdit.setDateTime(start)
		self.endDateTimeEdit.setDateTime(end)
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
	window = PassengerFlowReportFrame()
	window.show()
	sys.exit(app.exec_())