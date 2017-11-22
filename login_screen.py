import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import backend
import administrator_screen
import createAccount_screen
import welcomeToMarta_screen
import error_screen
import success_screen
import time

#File loads up GUI Frame described below - connects all buttons and clicks & ties functions to backend

qtCreatorFile = "ui/login.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class LoginFrame(QtWidgets.QFrame, Ui_Frame):
	def __init__(self):
		QtWidgets.QFrame.__init__(self)
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.loginButton.clicked.connect(self.VerifyLogin)
		self.registerButton.clicked.connect(self.OpenCreateAccount)
	def InitFromOtherFile(self,Ui_Frame):
		Ui_Frame.__init__(self)
		self.setupUi(self)
		self.loginButton.clicked.connect(self.VerifyLogin)
		self.registerButton.clicked.connect(self.OpenCreateAccount)
	def VerifyLogin(self): 
		username = str(self.usernameTextEdit.text())
		password = str(self.passwordTextEdit.text())
		out = backend.VerifyLogin(username,password)
		if out is None:
			self.error = "backend function failed"
			self.OpenError()
		else:
			if out == -1:
				self.error = "Invalid Username/Password"
				self.OpenError()
			else:
				self.success = "Logged In Successfully"
				self.OpenSuccess()
				if backend.is_admin:
					time.sleep(2)
					self.OpenAdministrator()
				else:
					time.sleep(2)
					self.OpenWelcomeToMarta()
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
		self.frame.UpdateText()
		self.frame.show()
	def OpenCreateAccount(self):
		self.frame = createAccount_screen.CreateAccountFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
	def OpenAdministrator(self): 
		self.frame = administrator_screen.AdministratorFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
	def OpenWelcomeToMarta(self):
		self.frame = welcomeToMarta_screen.WelcomeToMartaFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = LoginFrame()
	window.show()
	sys.exit(app.exec_())