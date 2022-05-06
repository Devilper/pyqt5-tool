import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.paths = ""
        self.setWindowTitle('文件拖入')  # ==> 窗口标题
        self.resize(500, 400)  # ==> 定义窗口大小
        ico_file = "../qt/ico/Ferrari.ico"
        self.setWindowIcon(QIcon(ico_file))
        self.textBrowser = QTextBrowser()
        self.setCentralWidget(self.textBrowser)
        self.setAcceptDrops(True)  # ==> 必须设置
        self.btn = QPushButton("清空", self)
        self.btn.setGeometry(200, 300, 100, 30)
        self.btn.clicked.connect(self.when_btn_click)

    def when_btn_click(self):
        self.textBrowser.setText("")

    def dragEnterEvent(self, event):
        file = event.mimeData().urls()[0].toLocalFile()
        if file not in self.paths:  # ==> 去重显示
            self.paths += file + "\n"
            print("拖拽的文件 ==> {}".format(file))
            self.textBrowser.setText(self.paths)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())