from Painter import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Paint()
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
