from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

from db.database import init_db


class TzDemo(QWidget):
    def __init__(self):
        super(TzDemo, self).__init__()

        self.setWindowTitle("拖拽案例")
        label1 = QLabel("请将左边标签名拖拽到右边")
        self.combo = MyComboBox()
        lineEdit = QLineEdit()
        lineEdit.setDragEnabled(True)  # 控件可拖动

        formLayout = QFormLayout()
        formLayout.addRow(label1)
        formLayout.addRow(lineEdit, self.combo)
        self.setLayout(formLayout)


class MyComboBox(QComboBox):
    window_closed = pyqtSignal()

    def __init__(self):
        super(MyComboBox, self).__init__()
        self.setAcceptDrops(True)
        self.list = []
        self.query_labels()

    def dragEnterEvent(self, event):
        # event: 被拖拽的事件
        # event.mimeData(), hasText() 判断触发事件中收否含有文本
        # 如果有，则event.accept()接收，如果没有，则event.ignore()不接收
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
    # 鼠标松开，释放控件时dropEvent事件自动触发
    # 将事件中的文本内容添加到下拉框列表中

    def dropEvent(self, event):
        text = event.mimeData().text()
        if text not in self.list:
            if query_label(text):
                self.list.append(text)
                self.addItem(event.mimeData().text())
                self.window_closed.emit()

    def query_labels(self):
        sql = "select * from label"
        result = init_db.query(sql)
        if result:
            for i in result:
                self.list.append(i[1])
                self.addItem(i[1])


def query_label(name):
    sql = "select * from label where name = ?"
    data = (name,)
    result = init_db.query(sql=sql, data=data)
    if result:
        return False
    else:
        create_sql = "insert into label (name) values (?)"
        create_data = (name,)
        init_db.create(create_sql, create_data)
        return True


