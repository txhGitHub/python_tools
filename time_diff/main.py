import sys
from PyQt5.QtWidgets import QApplication, QMainWindow 
from time_diff_ui import Ui_MainWindow  # 导入通过Qt Designer转换生成的Python文件
from PyQt5 import QtCore
from button_connect_process import Button_Connect_Process

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()  # 使用通过Qt Designer生成的类
        self.ui.setupUi(self)  # 设置用户界面
        self.button_connect_process = Button_Connect_Process(self.ui)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())