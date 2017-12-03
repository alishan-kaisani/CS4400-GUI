import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import backend
import error_screen
import success_screen

qtCreatorFile = "ui/breezeCardManagement.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class BreezeCardManagementFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.resetButton.clicked.connect(self.ResetFilter)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.setValueButton.clicked.connect(self.SetValue)
		self.transferCardButton.clicked.connect(self.TransferCard)
		self.CreateView('','',0,1000.00,False)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.resetButton.clicked.connect(self.ResetFilter)
		self.updateButton.clicked.connect(self.UpdateFilter)
		self.setValueButton.clicked.connect(self.SetValue)
		self.transferCardButton.clicked.connect(self.TransferCard)
		self.CreateView('','',0,1000.00,False)
	def UpdateView(self, owner, cardNum, minVal, maxVal, showSuspended): 
		self.hide()
		while (self.tableWidget.rowCount() > 0):
			self.tableWidget.removeRow(0)
		self.CreateView(owner, cardNum, minVal, maxVal, showSuspended)
		self.success = "Updated View!"
		self.show()
		self.OpenSuccess()
	def CreateView(self, owner, cardNum, minVal, maxVal, showSuspended):
		data = backend.BreezecardSearch(owner, cardNum, minVal, maxVal, showSuspended)

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
			if (data[i][2] == "Suspended" or data[i][2] == "Unassigned"):
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
		owner = str(self.ownerTextEdit.text())
		cardNum = str(self.cardNumberTextEdit.text())
		showSuspended = self.checkBox.isChecked()
		minVal = self.money1SpinBox.value()
		maxVal = self.money2SpinBox.value()
		validator = QtGui.QDoubleValidator(0,10000000000000000,0)

		if cardNum != '':
			if len(cardNum) != 16:
				self.error = "Not 16 digit input on cardNum"
				self.OpenError()
				return
			if (validator.validate(cardNum,0)[0] != 2):
				#validate() method returns  a tuple (QValiditatorState,QString,int) - look at first index in tuple
				#Qvalidator State is an enum: {0:"invlaid",1:"Intermediate",2:"Acceptable"}
				self.error = "Cardnumber is not valid - Must be 16 digits no spaces"
				self.OpenError()
				return

		self.UpdateView(owner,cardNum,minVal,maxVal,showSuspended)
	def SetValue(self): 
		if (self.CheckSelected() == -1):
			return
		row = self.tableWidget.selectedItems()[0].row()

		cardNum = self.tableWidget.item(row,0).data(0)
		cardNum = cardNum.replace(" ","")
		val = self.cardValueSpinBox.value()

		validator = QtGui.QDoubleValidator(1000000000000000,10000000000000000,0)
		if (validator.validate(cardNum,0)[0] != 2):
			#validate() method returns  a tuple (QValiditatorState,QString,int) - look at first index in tuple
			#Qvalidator State is an enum: {0:"invlaid",1:"Intermediate",2:"Acceptable"}
			self.error = "Cardnumber is not valid - Must be 16 digits no spaces"
			self.OpenError()
			return

		res = -1
		res = backend.SetCardValue(cardNum,val)

		if res == 1: 
			self.UpdateView('','',0,1000.00,False)
			# self.newframe.hide()
			self.success = "Value Updated!"
			self.OpenSuccess()
		elif res == -1:
			sel.error = "Error in Updating Card Value"
			self.OpenError()
			return
		else:
			self.error = "Unknown Error:\n" + str(res)
			self.OpenError()
			return
	def TransferCard(self): 
		if (self.CheckSelected() == -1):
			return
		row = self.tableWidget.selectedItems()[0].row()

		cardNum = self.tableWidget.item(row,0).data(0)
		cardNum = cardNum.replace(" ","")
		newOwner = str(self.transferTextEdit.text())

		if (newOwner == ""):
			self.error = "No owner specified"
			self.OpenError()
			return

		curOwner = backend.BreezeCardUser(cardNum)
		if curOwner != NULL:
			#passenger exists 
			if backend.PassengerInTrip(curOwner):
				self.error = "Passenger is in Trip. Wait to change card Owner"
				self.OpenError()
				return



		rest = -1
		res = backend.AssignCardToOwner(cardNum,newOwner)

		if res == 1:
			self.UpdateView('','',0,1000.00,False)
			self.newframe.hide()
			self.success = "Card Reassigned!"
			self.OpenSuccess()
		elif res == -1:
			self.error = "Error in Transfering Card"
			self.OpenError()
			return
		else:
			self.error = "Unkown Error\n" + str(res)
			self.OpenError()
			return
	def ResetFilter(self): 
		self.ownerTextEdit.setText("")
		self.cardNumberTextEdit.setText("")
		self.money1SpinBox.setValue(0.00)
		self.money2SpinBox.setValue(1000.00)
		self.checkBox.setChecked(False)
	def CheckSelected(self):
		if (len(self.tableWidget.selectedItems()) == 0):
			self.error = "No Card Selected"
			self.OpenError()
			return -1
		return 1
	def OpenError(self):
		self.newframe = error_screen.ErrorFrame()
		self.newframe.InitFromOtherFile(Ui_Frame)
		self.newframe.text = self.error
		self.newframe.UpdateText()
		self.newframe.show()
	def OpenSuccess(self):
		self.newframe = success_screen.SuccessFrame()
		self.newframe.InitFromOtherFile(Ui_Frame)
		self.newframe.text = self.success
		self.newframe.UpdateText()
		self.newframe.show()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = BreezeCardManagementFrame()
	window.show()
	sys.exit(app.exec_())