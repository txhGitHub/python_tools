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


class DoubleClickListViewExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.list_view = QListView(self)
        self.model = QStandardItemModel()
        for index in range(10000):
            item = QStandardItem('Item dd dd1  ' + str(index))
            item.setData((1, 2), Qt.UserRole) 
            self.model.appendRow(item)

        self.list_view.setModel(self.model)

        self.list_view.setEditTriggers(QListView.NoEditTriggers)  # 设置编辑触发器为NoEditTriggers

        delegate = CustomDelegate(self.list_view)
        self.list_view.setItemDelegate(delegate)  

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.list_view)
        self.setLayout(self.layout)

        self.setWindowTitle('Double Click ListView Example')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DoubleClickListViewExample()
    sys.exit(app.exec_())