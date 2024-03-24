from time_diff_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QTimer
import os
import re
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListView, QListView, QStyledItemDelegate
from PyQt5.QtCore import Qt,QEvent
from PyQt5.QtGui import QColor, QStandardItemModel, QStandardItem

class CustomDelegate(QStyledItemDelegate):  
    def __init__(self, parent=None):  
        super(CustomDelegate, self).__init__(parent)
        self.double_clicked_index_set = set()

    def editorEvent(self, event, model, option, index):
        if event.type() == QEvent.MouseButtonPress:
            if index.row() not in  self.double_clicked_index_set:
                self.double_clicked_index_set.add(index.row())
            else:
                self.double_clicked_index_set.remove(index.row())
        if event.type() == event.MouseButtonDblClick:
            # 获取双击的项的文本，到最前面，染色还需要重新处理
            tuple_data = index.model().data(index, Qt.UserRole)
            text = index.model().data(index, Qt.DisplayRole)
            item = QStandardItem(text)
            item.setData(tuple_data, Qt.UserRole) 
            print(text)
            # 将双击的项移动到最前面
            model.removeRow(index.row())
            model.insertRow(0, item)

        return super().editorEvent(event, model, option, index)

    def paint(self, painter, option, index):
                # 绘制默认背景 
        if index.row() in  self.double_clicked_index_set:
            painter.save()
            painter.fillRect(option.rect, QColor("lightblue"))  # 设置为浅蓝色背景
            painter.restore()
        # super(CustomDelegate, self).paint(painter, option, index)

        tuple_data = index.model().data(index, Qt.UserRole)
        text = index.model().data(index, Qt.DisplayRole)

        remaining_text_x = option.rect.left()
        fm = painter.fontMetrics()

        paintercount = 0
        for index in range(len(text)):
            if  tuple_data[0]  <= index and index <= tuple_data[1]:
                current_pen_color = painter.pen().color()
                if current_pen_color != QColor('red'):
                    painter.save()
                    painter.setPen(QColor('red'))
                    paintercount = paintercount + 1
            else:
                if paintercount != 0:
                    painter.restore()
                    paintercount = paintercount - 1
            text_width = fm.horizontalAdvance(text[index])
            # print(option.rect.left()) 
            painter.drawText(remaining_text_x , option.rect.top() + fm.ascent() , text[index])
            remaining_text_x = remaining_text_x + text_width


class Button_Connect_Process(object):
    def __init__(self, ui: Ui_MainWindow):
        self.ui = ui
        self.init_ui_components()
        self.create_connect()
        self.match_result = []
        self.model = QStandardItemModel()

    def show_message_box_with_qtimer(self, mesg: str) -> None:
        msg_box = QMessageBox()
        msg_box.setText(mesg)
        # msg_box.setWindowTitle("提示")
        msg_box.setStandardButtons(QMessageBox.Ok)
        # 定时器，1.5秒后关闭提示框
        timer = QTimer()
        timer.timeout.connect(msg_box.accept)
        timer.start(1500)
        msg_box.exec_()


    #对界面界面做初始化操作
    def init_ui_components(self):
        self.ui.result.setReadOnly(True)
        self.ui.re_lineEdit.setPlaceholderText("begin config|camxhal3.cpp")
        self.ui.re_lineEdit.setText("begin config|camxhal3.cpp")
        self.ui.filepath_lineEdit.setPlaceholderText("输入目录或者具体的文件路径")
        # self.ui.filepath_lineEdit.setText(r"C:\Users\pc\Desktop\test_log\log.txt")
        self.ui.filefilter_lineEdit.setPlaceholderText("文件以空格隔开，不输入默认搜索目录以及子目录所有文件")

    def initListView(self):
        if len(self.match_result) > 0:
            for result in self.match_result:
                item = QStandardItem(result[0])
                item.setData(result[1], Qt.UserRole) 
                self.model.appendRow(item)
        self.ui.line_listView.setModel(self.model)
        self.ui.line_listView.setEditTriggers(QListView.NoEditTriggers)  # 设置编辑触发器为NoEditTriggers
        delegate = CustomDelegate(self.ui.line_listView)
        self.ui.line_listView.setItemDelegate(delegate)

    def process_file(self, srcpath: str, restr: str):
        # 部分手机厂商log编码格式为：utf-16
        print(srcpath)
        with open(srcpath, 'r',  encoding='utf-16', errors='ignore') as file:
            line = file.readline()
            while line:
                matches = re.finditer(restr, line, re.IGNORECASE)
                for match in matches:
                    self.match_result.append((line, ( match.start(), match.end())))
                line = file.readline()

    def process_input_dir(self, srcpath: str):
        for root, dirs, files in os.walk(srcpath):
            for file in files:
                self.process_file(os.path.join(root, file),  self.ui.re_lineEdit.text())

    def process_search_event(self):
        if len(self.match_result) > 0:
            self.match_result.clear()
            self.model.clear()
        path : str  = self.ui.filepath_lineEdit.text()
        restr : str = self.ui.re_lineEdit.text()
        while True:
            if restr  is "":
                self.show_message_box_with_qtimer("需输入正则表达式")
                break

            if path is "":
                self.show_message_box_with_qtimer("输入文件或者文件目录")
                return
            # 需要对文件进行过滤，只看文本文档
            print(path)
            if os.path.isfile(path):
                self.process_file(path, self.ui.re_lineEdit.text())
                self.initListView()
                break

            if os.path.isdir(path):
                self.process_input_dir(path)
                self.initListView()
                break
            self.show_message_box_with_qtimer("请确定输入的路径是文件或者目录")
            break

    def create_connect(self) -> None:
        # 处理搜索点击事件
        self.ui.search_button.clicked.connect(self.process_search_event)
