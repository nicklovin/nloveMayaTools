from PySide2 import QtWidgets, QtCore, QtGui
from functools import partial
from pprint import pprint


# DynamicListWidget + Item reference taken from:
# https://robonobodojo.wordpress.com/2020/05/31/pyside2-custom-list-widgets/
class DynamicListWidgetItem(QtWidgets.QWidget):

    def __init__(self, label_text, size, margin=2):
        super(DynamicListWidgetItem, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        # self.setMaximumSize(1000, size+3)
        self.text = label_text
        self.widget_label = QtWidgets.QLabel(label_text)
        self.widget_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        self.button = QtWidgets.QPushButton('-')
        self.button.setFixedSize(QtCore.QSize(size, size))
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        layout = QtWidgets.QHBoxLayout()
        layout.setMargin(margin)
        layout.addWidget(self.widget_label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def get_value(self):
        return self.widget_label.text()


class DynamicListWidget(QtWidgets.QWidget):

    def __init__(self, token, size=20, item_size=15, input_type='text', input_options=[]):
        super(DynamicListWidget, self).__init__()
        self.setWindowTitle(f'{token} List')
        self.list_items = []
        self.token = token
        self.size = size
        self.item_size = item_size
        self.input_type = input_type
        self.input_options = input_options
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        self.layout.setContentsMargins(5, 1, 1, 1)
        self.setLayout(self.layout)

        self.add_item_button = QtWidgets.QPushButton('+')
        self.add_item_button.setFixedSize(QtCore.QSize(size, size))

        # List
        self.item_list_widget = QtWidgets.QListWidget()
        # self.item_list_widget.setVerticalScrollBarPolicy(QtGui.Qt.ScrollBarAlwaysOn)
        self.item_list_widget.setHorizontalScrollBarPolicy(QtGui.Qt.ScrollBarAlwaysOff)
        self.item_list_widget.setAlternatingRowColors(True)
        self.item_list_widget.setSizeAdjustPolicy(self.item_list_widget.AdjustToContents)
        self.item_list_widget.currentItemChanged.connect(self.current_item_changed)

        self.layout.addWidget(self.item_list_widget)
        self.layout.addWidget(self.add_item_button)
        self.add_item_button.clicked.connect(self.add_item)
        self.item_list_widget.itemDoubleClicked.connect(self.edit_item)
        # self.set_size()
        self.resize(self.sizeHint())

    def delete_button(self, sender):
        index = self.item_list_widget.row(sender)
        self.item_list_widget.takeItem(index)
        self.list_items.pop(index).deleteLater()
        pprint(self.list_items)

    def add_item(self):
        if self.input_type == 'text':
            text, ok = QtWidgets.QInputDialog.getText(self, f'Add {self.token}', f'{self.token} name')
        elif self.input_type == 'options':
            text, ok = QtWidgets.QInputDialog.getItem(self, f'Add {self.token}', f'{self.token} name', self.input_options, 0, False)
        else:
            raise NotImplementedError

        print(self)

        if ok:
            new_item = QtWidgets.QListWidgetItem()
            widget = DynamicListWidgetItem(str(text), self.item_size)
            widget.button.clicked.connect(partial(self.delete_button, new_item))
            new_item.setSizeHint(widget.sizeHint())
            self.item_list_widget.addItem(new_item)
            self.item_list_widget.setItemWidget(new_item, widget)
            self.item_list_widget.setCurrentItem(new_item)
            self.list_items.append(widget)

        print(self.list_items)

    def set_input_options(self, options):
        self.input_options = options

    @property
    def current_value(self):
        if self.item_list_widget.currentItem():
            return self.item_list_widget.itemWidget(self.item_list_widget.currentItem()).text
        else:
            return None

    def current_item_changed(self):
        # print(self.current_value)
        pass

    def edit_item(self):
        pass

    def get_items(self):
        return self.list_items

    def clear(self):
        self.item_list_widget.clear()
        self.list_items = []
