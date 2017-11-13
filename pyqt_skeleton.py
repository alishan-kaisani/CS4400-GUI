import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets

qtCreatorFile = "" # Enter file here.

Ui_Frame, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QFrame, Ui_Frame):
    def __init__(self):
        QtWidgets.QFrame.__init__(self)
        Ui_Frame.__init__(self)
        self.setupUi(self)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())