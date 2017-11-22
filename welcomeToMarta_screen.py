import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import error_screen
import success_screen

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
	def ManageCards(self, event): 
		self.error = "ManageCards Function Not Defined Yet"
		self.OpenError()
	def EndTrip(self, event): 
		self.error = "EndTrip Function Not Defined Yet"
		self.OpenError()
	def ViewTripHistory(self):
		self.error = "ViewTripHistory Function Not Defined Yet"
		self.OpenError()
	def LogOut(self): 
		self.error = "LogOut Function Not Defined Yet"
		self.OpenError()
	def OpenError(self):
		self.frame = error_screen.ErrorFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.text = self.error
		self.frame.UpdateText()
		self.frame.show()
	def OpenSuccess(self):
		self.frame = success_screen.SuccessFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.text = self.success;
		self.UpdateText()
		self.frame.show()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = WelcomeToMartaFrame()
	window.show()
	sys.exit(app.exec_())