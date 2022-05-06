import sys

from PyQt5.QtWidgets import *

from db.database import init_db
from image_list import ImageWidget
from qt_ui import search


class SearchWindow(QMainWindow, search.Ui_MainWindow):

    def __init__(self):
        super(SearchWindow, self).__init__()
        self.setupUi(self)
        self.image_widget = ImageWidget(self, col=4, w=750, h=500)
        self.image_widget.move(25, 70)
        self.upButton.clicked.connect(lambda: self.image_widget.turn_page(-1))
        self.downButton.clicked.connect(lambda: self.image_widget.turn_page(1))  # 图像列表翻页
        self.image_widget.signal_order.connect(self.change_path)
        self.image_widget.signal_page.connect(self.change_page)
        # self.image_widget.signal_open.connect(self.change_model)
        self.searchButton.clicked.connect(self.search)
        self.init_box()

    def change_path(self, path):
        # 选择一个文件
        dir_ = QFileDialog.getOpenFileName(self, "选取文件", path, "All Files(*)")

    def change_page(self, index):
        ...

    def change_model(self, path):
        # todo 获取path大小
        dir_ = QFileDialog.getExistingDirectory(self, "选取文件夹", path)

    def init_box(self):
        sql = "select * from label"
        result = init_db.query(sql)
        if result:
            self.comboBox.clear()
            for i in result:
                self.comboBox.addItem(i[1])

    def search(self):
        label = self.comboBox.currentText()
        name = self.lineEdit.text()
        if name and label:
            data = (label, f"%{name}%")
            sql = "select * from info where l_name =? and name like ?"
        elif name:
            data = (f"%{name}%",)
            sql = "select * from info where name like ?"
        elif label:
            data = (label,)
            sql = "select * from info where l_name = ?"
        else:
            data = None
            sql = "select * from info"
        result = init_db.query(sql, data=data)
        list_files = []
        list_models = []
        if result:
            for i in result:
                if i[2]:
                    list_files.append(i[2])
                    list_models.append(i[3])
        self.image_widget.list_files = list_files
        self.image_widget.list_models = list_models
        self.image_widget.show_images_list()



