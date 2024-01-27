# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from PyQt5.QtWidgets import QApplication
import mainwindow

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Subclass QMainWindow to customize your application's main window

    app = QApplication(sys.argv)

    window = mainwindow.MainWindow()
    window.show()

    app.exec()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
