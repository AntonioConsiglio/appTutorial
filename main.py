import sys

from PySide2.QtWidgets import QApplication
from application import HomeScreen


def main():
    app = QApplication(sys.argv)

    root = HomeScreen()
    root.show()
    
    app.exit(app.exec_())

if __name__ == '__main__':
    main()