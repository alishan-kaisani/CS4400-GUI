import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import backend
import administrator_screen
import createAccount_screen
import welcomeToMarta_screen

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
		username = str(self.usernameTextEdit.toPlainText())
		password = str(self.passwordTextEdit.toPlainText())
		out = backend.VerifyLogin(username,password)
		print(type(out));
		if out[0] == -1:
			print('error')
		else:
			if is_admin:
				self.OpenAdministrator()
			else:
				self.OpenWelcomeToMarta()
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
	def OpenWelcomeToMarta():
		self.frame = welcomeToMarta_screen.WelcomeToMartaFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	window = LoginFrame()
	window.show()
	sys.exit(app.exec_())