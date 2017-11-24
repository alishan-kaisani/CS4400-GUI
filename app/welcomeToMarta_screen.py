import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen
import login_screen
import manageCards_screen
import tripHistory_screen

qtCreatorFile = "ui/welcomeToMarta.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class WelcomeToMartaFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.manageCardsLabel.mousePressEvent = self.ManageCards
		self.endTripLabel.mousePressEvent= self.EndTrip
		self.viewTripHistoryButton.clicked.connect(self.ViewTripHistory)
		self.logOutButton.clicked.connect(self.LogOut)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.manageCardsLabel.mousePressEvent = self.ManageCards
		self.endTripLabel.mousePressEvent= self.EndTrip
		self.viewTripHistoryButton.clicked.connect(self.ViewTripHistory)
		self.logOutButton.clicked.connect(self.LogOut)
	def PopulateBreezeCards(self): 
		cardList = backend.getBreezeCards()
		#backend function that returns a list of breezecard numbers
		newList = []
		for card in cardlist: 
			card = str(card)
			newList.append(card)
		self.breezeCardBox.addItems(newList)
	def UpdateBreezeCard(self): 
		cur_breezeCard = int(self.breezeCardBox.currentText())
		details = breezeCard.GetBreezeCardInfo(cur_brezecard)
		self.balanceAmount.setText("$" + details["Money"])

		#Fill in Start at Values

		#Fill in Trip Progress Label

		#Fill in End at Values
	def ManageCards(self, event): 
		self.frame = manageCards_screen.ManageCardsFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
	def EndTrip(self, event): 
		self.error = "EndTrip Function Not Defined Yet"
		self.OpenError()
	def ViewTripHistory(self):
		self.frame = tripHistory_screen.TripHistoryFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()	
	def LogOut(self): 
		self.frame = login_screen.LoginFrame()
		self.frame.InitFromOtherFile(Ui_Frame) 
		self.frame.show()
		self.hide()
		self.success = "Logged Out Successfully"
		self.OpenSuccess()
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
	window = WelcomeToMartaFrame()
	window.show()
	sys.exit(app.exec_())