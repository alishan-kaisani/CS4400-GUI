import sys
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

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
		print("Managing Cards...")
	def EndTrip(self, event): 
		print("Ending Trip...")
	def ViewTripHistory(self):
		print("Viewing Trip History...")
	def LogOut(self): 
		print("Logging Out")

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = WelcomeToMartaFrame()
	window.show()
	sys.exit(app.exec_())