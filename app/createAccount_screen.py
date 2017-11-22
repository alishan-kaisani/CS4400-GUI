import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import login_screen
import error_screen
import login_screen

qtCreatorFile = "ui/createAMartaAccount.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class CreateAccountFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createAnAccountButton.clicked.connect(self.CreateAccount)
		self.existingBreezecardButton.toggled.connect(self.ExistingRadioClicked)
		self.newBreezecardButton.toggled.connect(self.NewRadioClicked)
	def ExistingRadioClicked(self,enabled):
		if enabled:
			self.cardNumberTextEdit.setEnabled(True)
	def NewRadioClicked(self,enabled):
		if enabled:
			self.cardNumberTextEdit.setEnabled(False)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.createAnAccountButton.clicked.connect(self.CreateAccount)
		self.existingBreezecardButton.toggled.connect(self.ExistingRadioClicked)
		self.newBreezecardButton.toggled.connect(self.NewRadioClicked)
	def CreateAccount(self):
		username = self.usernameTextEdit.toPlainText()
		email = self.emailAddressTextEdit.toPlainText()
		password = self.passwordTextEdit.toPlainText()
		confirmPassword = self.confirmPasswordTextEdit.toPlainText()
		newCard = self.newBreezecardButton.isChecked()
		existingCard = self.existingBreezecardButton.isChecked()
		#Should assert that newCard == ~existingCard
		out = backend.CreateAccount(username,email,password,confrimPassword,newCard,existingCard)
		if out is None: 
			self.error = "error in Backend"
			self.OpenError()
		else:
			if out == 1:
				self.success = "Account created Successfully"
				self.OpenLogin()
				self.OpenSuccess()
			else:
				self.error = "Error in Account Creation"
				self.OpenError()
	def OpenLogin(self): 
		self.frame = login_screen.LoginFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
	def OpenError(self):
		self.frame = error_screen.ErrorFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.text = self.error;
		self.UpdateText()
		self.frame.show()
	def OpenSuccess(self):
		self.frame = success_screen.SuccessFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.text = self.success;
		self.UpdateText()
		self.frame.show()



if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = CreateAccountFrame()
	window.show()
	sys.exit(app.exec_())