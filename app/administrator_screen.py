import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import stationListing_screen
import suspendedCards_screen
import breezeCardManagement_screen
import passengerFlowReport_screen
import login_screen
import success_screen

qtCreatorFile = "ui/administrator.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class AdministratorFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.stationManagementButton.clicked.connect(self.OpenStationManagement)
		self.suspendedCardsButton.clicked.connect(self.OpenSuspendedCards)
		self.breezeCardManagementButton.clicked.connect(self.OpenBreezeCardManagement)
		self.passengerFlowReportButton.clicked.connect(self.OpenPassengerFlowReport)
		self.logOutButton.clicked.connect(self.LogOut)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.stationManagementButton.clicked.connect(self.OpenStationManagement)
		self.suspendedCardsButton.clicked.connect(self.OpenSuspendedCards)
		self.breezeCardManagementButton.clicked.connect(self.OpenBreezeCardManagement)
		self.passengerFlowReportButton.clicked.connect(self.OpenPassengerFlowReport)
		self.logOutButton.clicked.connect(self.LogOut)
	def OpenStationManagement(self):
		self.frame = stationListing_screen.StationListingFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		print("opening station management...\n")
	def OpenSuspendedCards(self): 
		self.frame = suspendedCards_screen.SuspendedCardsFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		print("opening suspended cards...\n")
	def OpenBreezeCardManagement(self): 
		self.frame = breezeCardManagement_screen.BreezeCardManagementFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		print("opening breeze card management...\n")
	def OpenPassengerFlowReport(self):
		self.frame = passengerFlowReport_screen.PassengerFlowReportFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		print("opening passenger flow report...\n")
	def LogOut(self):
		self.frame = login_screen.LoginFrame()
		self.frame.InitFromOtherFile(Ui_Frame) 
		self.frame.show()
		self.hide()
		self.success = "Logged Out Successfully"
		self.OpenSuccess()
	def OpenSuccess(self):
		self.newframe = success_screen.SuccessFrame()
		self.newframe.InitFromOtherFile(Ui_Frame)
		self.newframe.text = self.success
		self.newframe.UpdateText()
		self.newframe.show()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = AdministratorFrame()
	window.show()
	sys.exit(app.exec_())