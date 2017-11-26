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
		#out = backendFunc(username,password)		
		out = backend.VerifyLogin(str(self.usernameTextEdit.text()),str(self.passwordTextEdit.text()))
		if out is None:
			self.error = "backend function failed"
			self.OpenError()
			return
		else:
			if out == -1:
				self.error = "Invalid Username/Password"
				self.OpenError()
				return
			else:
				self.success = "Logged In Successfully\nUsername: %s" % (backend.passenger_username) 
				if backend.is_admin:
					self.OpenAdministrator()
				else:
					self.OpenWelcomeToMarta()
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
	def OpenCreateAccount(self):
		self.frame = createAccount_screen.CreateAccountFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
	def OpenAdministrator(self): 
		self.frame = administrator_screen.AdministratorFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		geometry = self.frame.geometry() #Returns a QRect object that containins window details
		geometry.moveTo(175,225)
		self.frame.setGeometry(geometry)
		self.frame.show()
		self.hide()
	def OpenWelcomeToMarta(self):
		self.frame = welcomeToMarta_screen.WelcomeToMartaFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		geometry = self.frame.geometry() #Returns a QRect object that containins window details
		geometry.moveTo(175,225)
		self.frame.setGeometry(geometry)
		self.frame.show()
		self.hide()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = LoginFrame()
	window.show()
	sys.exit(app.exec_())