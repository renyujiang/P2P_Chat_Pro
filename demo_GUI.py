import sys

from PyQt5 import QtWidgets, uic

# Load the UI file
Ui_MainWindow, QtBaseClass = uic.loadUiType("./GUI/comm_gui.py")


# Create a PyQt widget based on the UI
class MyWidget(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


# Create and show the widget
app = QtWidgets.QApplication(sys.argv)
widget = MyWidget()
widget.show()
sys.exit(app.exec_())
