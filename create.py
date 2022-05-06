from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLineEdit, QLabel, QFormLayout, QMessageBox

from db.database import init_db
from qt_ui import create


class CreateWindow(create.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(CreateWindow, self).__init__()
        self.setupUi(self)
        self.label_set = set()
        self.paths = ""
        self.setAcceptDrops(True)
        self.saveImage.clicked.connect(self.image_path)  # 存图片按钮
        self.saveModel.clicked.connect(self.model_path)  # 存模型按钮
        self.init_label_box()
        self.addButton.clicked.connect(self.save_info)  # 保存信息
        self.image_url = ""
        self.model_url = ""
        self.name = ""
        self.label_name = ""

    def init_label_box(self):
        sql = "select * from label"
        result = init_db.query(sql)
        if result:
            self.labelBox.clear()
            for i in result:
                self.labelBox.addItem(i[1])

    def image_path(self):
        path = _get_base_path()
        fname, _ = QFileDialog.getOpenFileName(self, '选择图片', path, 'Image files(*.jpg *.gif *.png)')
        self.image_url = fname
        print(self.image_url)
        self.image.setPixmap(QPixmap(fname).scaled(240, 240))
        self.image.setScaledContents(True)

    def model_path(self):
        path = _get_base_path()
        directory = QFileDialog.getExistingDirectory(None, "选取文件夹", path)  # 起始路径
        self.model_url = directory
        self.textBrowser.setText(directory)

    def save_info(self):
        # 保存到数据库
        option_text = self.labelBox.currentText()
        text = self.nameEdit.text()
        if all((option_text, text, self.image_url, self.model_url)):
            data = (text, option_text, self.image_url, self.model_url)
            sql = f"insert into info (name, l_name, img, model) values (?,?,?,?)"
            init_db.create(sql=sql, data=data)
            self.image_url = ""
            self.model_url = ""
            self.nameEdit.setText("")
            self.image.setPixmap(QPixmap(""))
            self.textBrowser.setText("")

            messageDialog('info', "提示", "保存成功")
        else:
            messageDialog('waring', "告警", "数据必填")


def messageDialog(type, tips, info):
    if type == 'info':
    # 核心功能代码就两行，可以加到需要的地方
        msg_box = QMessageBox(QMessageBox.Information, tips, info)
    elif type == 'waring':
        msg_box = QMessageBox(QMessageBox.Warning, tips, info)
    else:
        msg_box = QMessageBox(QMessageBox.Abort, "错误", "错误提示")
    msg_box.exec_()


def _get_base_path():
    sql = "select * from path"
    result = init_db.query(sql)
    if result:
        path = result[0][1]
    else:
        path = "./"
    return path
