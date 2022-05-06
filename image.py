from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel


class Image(QWidget):
    def __init__(self, x=600, y=800):
        super(Image, self).__init__()
        self.move(0, 0)
        self.lbl = QLabel("图片", self)
        self.lbl.setScaledContents(True)

    def myAddPic(self, img):
        pm = QPixmap(img)
        self.lbl.setPixmap(pm)

