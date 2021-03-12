from PyQt5.QtWidgets import QApplication
from game import Gomoku
from window import GomokuWindow
import sys

def main():
    # g = Gomoku()
    # g.play()
    app = QApplication(sys.argv)
    ex = GomokuWindow()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main() 