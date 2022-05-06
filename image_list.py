# -*- coding: utf-8 -*-
import logging

from PyQt5.QtWidgets import QWidget, QApplication, QMessageBox, QLabel, QHBoxLayout, QFrame, QGridLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, Qt
import sys, os, math

from db.database import init_db
from image import Image



class ImageWidget(QWidget):
    group_num = 1  # 图像列表当前组数（页数）
    list_files = []  # 图像文件路径集
    list_models = []
    signal_order = pyqtSignal(str)  # 图像项目信号
    signal_page = pyqtSignal(int)  # 页数信号
    signal_open = pyqtSignal(str)  # 模型信号

    def __init__(self, parent=None, col=1, w=10, h=None, suit=0):
        super(ImageWidget, self).__init__(parent)
        self.get_files()
        self.col = col
        self.w = w
        self.suit = suit
        if h == None:
            self.h = self.w / self.col
        else:
            self.h = h
        self.positions = [(i, j) for i in range(2) for j in range(2)]
        self.setFixedSize(self.w, self.h)
        self.hbox = QGridLayout(self)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        self.show_images_list()  # 初次加载形状图像列表

    def get_files(self):  # 储存当前页需加载的图像路径
        # 查询数据库
        sql = "select * from info"
        result = init_db.query(sql)
        if result:
            for i in result:
                if i[2]:
                    self.list_files.append(i[2])
                    self.list_models.append(i[3])

    def show_images_list(self):  # 加载图像列表
        for i in range(self.hbox.count()):  # 每次加载先清空内容，避免layout里堆积label
            self.hbox.itemAt(i).widget().deleteLater()
        # 设置分段显示图像，每col个一段
        group_num = self.group_num
        start = 0
        end = self.col
        if group_num > 1:
            start = self.col * (group_num - 1)
            end = self.col * group_num
        count = 0  # 记录当前页载入的label数
        width = 150  # 自定义label宽度
        height = self.h  # 自定义label高度

        for index, path in enumerate(self.list_files):  # group_num = 1 则加载前col个，以此类推
            if index < start:
                continue
            elif index == end:
                break
            label = MyLabel(index)
            # 按路径读取成QPixmap格式的图像，根据适应方式调整尺寸
            logging.debug(f"suit:{self.suit}")
            if self.suit == 0:
                width = height = min(int(label.size().width() / 2), int(label.size().height() / 2))
                logging.debug(f"label:{label.size()}")
                logging.debug(f"label width:{width}")
                logging.debug(f"label height:{height}")
                pix = QPixmap(path).scaled(int(366), int(241))
                # pix = QPixmap(path)

            elif self.suit == 1:

                pix = QPixmap(path)
                pix = QPixmap(path).scaled(int(pix.width()*height/pix.height())-2*self.col, height-4)
            elif self.suit == 2:

                pix = QPixmap(path)
                pix = QPixmap(path).scaled(width-2*self.col, int(pix.height()*width/pix.width())-4)
                # pix = QPixmap(path).scaled(240, 240)

            label.setPixmap(pix)  # 加载图片
            self.hbox.addWidget(label, *self.positions[index % self.col])   # 在水平布局中添加自定义label
            label.signal_order.connect(self.choose_image)  # 绑定自定义label点击信号
            count += 1
        if not count == self.col:
            for i in range(self.col - count):
                label = QLabel()
                self.hbox.addWidget(label)  # 在水平布局中添加空label补位

    def turn_page(self, num):  # 图像列表翻页
        flag = len(self.list_files)
        if self.group_num == 1 and num == -1:  # 到首页时停止上翻
            QMessageBox.about(self, "Remind", "这是第一页!")
        elif (self.group_num == math.ceil(flag/self.col) and num == 1) or flag == 0:  # 到末页时停止下翻
            QMessageBox.about(self, "Remind", "没有更多图片! ")
        else:
            self.group_num += num  # 翻页
        self.signal_page.emit(self.group_num)
        self.show_images_list()  # 重新加载图像列表

    def choose_image(self, index):  # 选择图像
        # 选择地址
        self.signal_order.emit(self.list_models[index])
        # self.signal_open.emit(self.list_files[index])


class MyLabel(QLabel):  # 自定义label，用于传递是哪个label被点击了
    signal_order = pyqtSignal(int)
    signal_open = pyqtSignal(int)

    def __init__(self, order=None):
        super(MyLabel, self).__init__()
        self.order = order
        self.setStyleSheet("border-width: 2px; border-style: solid; border-color: gray")

    def mousePressEvent(self, e):  # 重载鼠标点击事件
        if e.buttons() == Qt.LeftButton:
            self.signal_order.emit(self.order)
            print("左")

        elif e.buttons() == Qt.RightButton:
            print("右")
            self.signal_open.emit(self.order)
