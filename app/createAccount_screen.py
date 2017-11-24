import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import login_screen
import error_screen
import login_screen
import backend

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
		#Read out data into vars
		username = self.usernameTextEdit.text()
		email = self.emailAddressTextEdit.text()
		password = self.passwordTextEdit.text()
		confirmPassword = self.confirmPasswordTextEdit.text()

		#Create QIntValidator to check carndumber is 16 digits later in code
		validator = QtGui.QIntValidator(1e15,1e16)

		#Check all possible Error conditions
		if (username == "" or email == "" or password == "" or confirmPassword == ""):
			self.error = "All fields must be filled"
			self.OpenError()
			return

		if password != confirmPassword:
			self.error = "Password doesn't match Confirm Password"
			self.OpenError()
			return

		if (len(password) < 8):
			#password must be atleast 8 characters long
			self.error = "Pasword must be atleast 8 characters"
			self.OpenError()

		if ((not (self.newBreezecardButton.isChecked())) and (not (self.existingBreezecardButton.isChecked()))):
			#Condition checks if neither radiobutton is checked
			self.error = "All Passengers need atleast 1 breezecard"
			self.OpenError()
			return

		res = -1;
		if self.newBreezecardButton.isChecked():
			#Condition checks if new breezecard is being used
			res = backend.CreateNewUser(username,email,password)
		elif self.existingBreezecardButton.isChecked():
			cardnumber = self.cardNumberTextEdit.text()
			if (cardnumber == ""):
				self.error = "Card Number Field Empty"
				self.OpenError()
				return;
			if (validator.validate(cardnumber,0)[0] != 2):
				#validate() method returns  a tuple (QValiditatorState,QString,int) - look at first index in tuple
				#Qvalidator State is an enum: {0:"invlaid",1:"Intermediate",2:"Acceptable"}
				self.error = "Cardnumber is not valid - Must be 16 digits no spaces"
				self.OpenError()
				return
			res = backend.CreateNewUser(username,email,password,cardnumber)

		if res == 1: 
			self.success = "Account created Successfully"
			self.OpenLogin()
			self.OpenSuccess()
		elif res == -1:
			self.error = "Error in Account Creation"
			self.OpenError()
			return
		else:
			self.error = "Unknown Error"
			self.openError()
	def OpenLogin(self): 
		self.frame = login_screen.LoginFrame()
		self.frame.InitFromOtherFile(Ui_Frame)
		self.frame.show()
		self.hide()
	def OpenError(self):
		self.newframe = error_screen.ErrorFrame()
		self.newframe.InitFromOtherFile(Ui_Frame)
		self.newframe.text = self.error;
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
	window = CreateAccountFrame()
	window.show()
	sys.exit(app.exec_())