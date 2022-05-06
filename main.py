import logging
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog  # 必须使用这两个类

from create import CreateWindow
from db.database import init_table, init_db
from label import TzDemo
from log import init_log
from qt_ui.home import Ui_MainWindow
from search import SearchWindow


class HomeWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(HomeWindow, self).__init__()
        self.setupUi(self)
        init_log()
        init_table()
        self.pathButton.clicked.connect(self.set_path)

    def set_path(self):
        sql = "select * from path"
        result = init_db.query(sql)
        logging.debug(f"path query:{result}")

        if result:
            path = result[0][1]
            id = result[0][0]
        else:
            path = "./"
            id = 0

        path_dir = QFileDialog.getExistingDirectory(self, "选取文件夹", path)
        if path_dir and path_dir != path:
            if id == 0:
                create_sql = "insert into path (name) values (?)"
                data = (path_dir,)
                init_db.create(sql=create_sql, data=data)
            else:
                update_sql = "update path set name = ? where id = ?"
                data = (path_dir, id)
                logging.debug(f"update path data:{data}")
                init_db.create(sql=update_sql, data=data)


if __name__ == '__main__':
    # 创建QApplication
    app = QApplication(sys.argv)  # sys获得命令行参数

    # 创建窗口
    main_window = HomeWindow()
    create_window = CreateWindow()
    search_window = SearchWindow()
    label_window = TzDemo()

    # 主页显示
    main_window.show()

    main_window.saveButton.clicked.connect(create_window.show)
    main_window.searchButton.clicked.connect(search_window.show)
    create_window.pushButton.clicked.connect(label_window.show)
    label_window.combo.window_closed.connect(create_window.init_label_box)
    label_window.combo.window_closed.connect(search_window.init_box)
    sys.exit(app.exec_())



