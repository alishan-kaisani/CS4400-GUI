import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

qtCreatorFile = "login.ui" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QFrame, Ui_Frame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        Ui_Frame.__init__(self)
        self.setupUi(self)
        self.loginButton.clicked.connect(self.VerifyLogin)
    def VerifyLogin(self): 
    	username = str(self.usernameTextEdit.toPlainText())
    	password = str(self.passwordTextEdit.toPlainText())



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())