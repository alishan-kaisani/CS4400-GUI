import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen
import backend

qtCreatorFile = "ui/manageCards.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class ManageCardsFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.addCardButton.clicked.connect(self.AddCard)
		self.addValueButton.clicked.connect(self.AddValue)
		#self.CreateView()
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.addCardButton.clicked.connect(self.AddCard)
		self.addValueButton.clicked.connect(self.AddValue)
		self.CreateView()
	def AddCard(self): 
		cardNum = str(self.cardNumberTextEdit.text())
		#Specfies range of 1e15 to 1e16 to cover all possible 16 digit numbers
		validator = QtGui.QDoubleValidator(1000000000000000,10000000000000000,0)

		if (validator.validate(cardNum,0)[0] != 2):
			self.error = "BreezeCard Numbers must be 16 digits - no spaces"
			self.OpenError()
			return

		res = -1
		res = backend.AddBreezeCard(cardNum)

		if res == 1: 
			self.success = "Card Added Successfully"
			self.hide()
			self.OpenSuccess()
			self.show()
		elif res == -1:
			self.error = "Error in Adding BreezeCard"
			self.OpenError()
			return
		else:
			self.error = "Unknown Error:\n" + str(res)
			self.OpenError()
	def AddValue(self): 
		if (len(self.tableWidget.selectedItems()) == 0):
			self.error = "No Card Selected"
			self.OpenError()
			return

		cardNum = str(self.creditCardNumberTextEdit.text())
		value = cardValueSpinBox.value
		validator = QtGui.QIntValidator(1e15,1e16)

		if (validator.validate(cardNum,0)[0] != 2):
			self.error = "BreezeCard Numbers must be 16 digits - no spaces"
			self.OpenError()
			return

		row_ndx = self.tableWidget.selectedItems()[0].row()
		breezeCardNum = self.tableWdiget.item(row_ndx,0)

		res = -1
		res = backend.AddValue(breezeCardNum, cardNum, value)

		if res == 1: 
			self.success = "Card Added Successfully"
			self.hide()
			self.OpenSuccess()
			self.show()
		elif res == -1:
			self.error = "Error in Adding BreezeCard"
			self.OpenError()
			return
		else:
			self.error = "Unknown Error:\n" + str(res)
			self.OpenError()
	def CreateView(self):
		data = backend.ViewPassengerCards()
		self.tableWidget.setRowCount = len(data)
		font = QtGui.Qfont()
		font.setUnderline()
		for i in range(0,len(data)):
			self.tableWidget.insertRow(i)
			for j in range(0,self.tableWidget.columnCount()):
				if j == 0: 
					#if dealing with breezecard #.. insert spaces
					cardNum = str(data[i][j])
					cardNum = str[0:4] + " " + str[4:8] + " " + str[8:12] + " " + str[12:16]
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(cardNum))
				elif j == 1:
					#if dealing with card values.. adjust formating 
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem("$"+"{0:.2f}".format(data[i][j])))
				else:
					self.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem("Remove"))
					self.tableWidget.item(i,j).setFont(font)
		self.tableWidget.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)
		self.tableWidget.horizontalHeader().setSectionResizeMode(1,QtWidgets.QHeaderView.ResizeToContents)
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
	window = ManageCardsFrame()
	window.show()
	sys.exit(app.exec_())