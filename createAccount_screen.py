import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import login_screen

qtCreatorFile = "ui/createAMartaAccount.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CreateAccountFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createAnAccountButton.clicked.connect(self.CreateAccount)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createAnAccountButton.clicked.connect(self.CreateAccount)
	def CreateAccount(self):
		username = self.usernameTextEdit.toPlainText()
		email = self.emailAddressTextEdit.toPlainText()
		password = self.passwordTextEdit.toPlainText()
		confirmPassword = self.confirmPasswordTextEdit.toPlainText()
		newCard = self.newBreezecardButton.isChecked()
		existingCard = self.existingBreezecardButton.isChecked()
		#Should assert that newCard == ~existingCard
		print("creating an account...")
		self.OpenLogin()
	def OpenLogin(self): 
		self.frame = login_screen.LoginFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()


if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = CreateAccountFrame()
	window.show()
	sys.exit(app.exec_())