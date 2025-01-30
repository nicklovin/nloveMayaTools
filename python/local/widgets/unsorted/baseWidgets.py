from PySide2 import QtWidgets, QtCore, QtGui


class AspectRatioWidget(QtWidgets.QWidget):

    def __init__(self, widget, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.widget = widget
        self.aspect_ratio = self.widget.size().width() / self.widget.size().height()
        self.setLayout(QtWidgets.QBoxLayout(QtWidgets.QBoxLayout.LeftToRight, self))
        self.layout().setContentsMargins(1, 1, 1, 1)
        #  add spacer, then widget, then spacer
        self.layout().addItem(QtWidgets.QSpacerItem(0, 0))
        self.layout().addWidget(self.widget)
        self.layout().addItem(QtWidgets.QSpacerItem(0, 0))

    def resizeEvent(self, e):
        w = e.size().width()
        h = e.size().height()

        if w / h > self.aspect_ratio:  # too wide
            self.layout().setDirection(QtWidgets.QBoxLayout.LeftToRight)
            widget_stretch = h * self.aspect_ratio
            outer_stretch = (w - widget_stretch) / 2 + 0.5
        else:  # too tall
            self.layout().setDirection(QtWidgets.QBoxLayout.TopToBottom)
            widget_stretch = w / self.aspect_ratio
            outer_stretch = (h - widget_stretch) / 2 + 0.5

        self.layout().setStretch(0, outer_stretch)
        self.layout().setStretch(1, widget_stretch)
        self.layout().setStretch(2, outer_stretch)


class ColumnWidget(QtWidgets.QWidget):
    def __init__(self, parent=None, column_count=2, column_sizes=[], *args, **kwargs):
        super(ColumnWidget, self).__init__(parent=parent)

        self.columns = {}
        if not column_sizes:
            column_sizes = [0 for i in range(column_count)]
        self.column_sizes = column_sizes
        self.column_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.column_layout)

        self.build_columns(column_count)

    def build_columns(self, count):
        for col in range(count):
            column = QtWidgets.QWidget()
            column_layout = QtWidgets.QVBoxLayout()
            column.setLayout(column_layout)

            column.setMinimumWidth(self.column_sizes[col])

            self.columns[col] = column_layout
            self.column_layout.addWidget(column)

    def get_column(self, col_num):
        return self.columns[col_num]

    def addWidget(self, widget, col_num):
        column = self.get_column(col_num)
        column.addWidget(widget)

    def addSpacerItem(self, widget, col_num):
        column = self.get_column(col_num)
        column.addSpacerItem(widget)


class FilteredList(QtWidgets.QWidget):

    def __init__(self, parent=None, filter_widget=None, *args, **kwargs):
        super(FilteredList, self).__init__(parent=parent)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinAndMaxSize)
        self.layout.setContentsMargins(5, 1, 1, 1)
        self.setLayout(self.layout)

        self.items = []

        self.filter_widget = filter_widget

        self.widget = QtWidgets.QListWidget()
        # self.widget.setVerticalScrollBarPolicy(QtGui.Qt.ScrollBarAlwaysOn)
        # self.widget.setHorizontalScrollBarPolicy(QtGui.Qt.ScrollBarAlwaysOff)
        self.widget.setAlternatingRowColors(True)
        self.widget.setSizeAdjustPolicy(self.widget.AdjustToContents)
        self.widget.currentItemChanged.connect(self.current_item_changed)

        self.layout.addWidget(self.widget)

        self._set_filter_policy()

        self.resize(self.sizeHint())

    def _set_filter_policy(self):
        if not self.filter_widget:
            self.filter_widget = QtWidgets.QLineEdit()
            self.layout.addWidget(self.filter_widget)
        else:
            pass
            # if not isinstance(self.filter_widget, QtWidgets.QLineEdit):
            #     raise TypeError('Invalid widget type for filter widget!  Must be QLineEdit (or wrapper of such)')

        self.filter_widget.textChanged.connect(self._filter_list)

    def _filter_list(self):
        input_text = str(self.filter_widget.text())
        print(input_text)
        if input_text == '':
            for item in self.items:
                item.setHidden(False)
        else:
            for item in self.items:
                item.setHidden(not(item.filter_by_text(input_text)))

    def current_item_changed(self):
        row = self.widget.currentRow()
        print(self.items[row].get_value())

    def add_items(self, items):
        if isinstance(items[0], str):
            widget_items = [ListWidgetItem(item) for item in items]
        else:
            widget_items = items

        for item in widget_items:
            self.widget.addItem(item)
            self.widget.setItemWidget(item, item.widget_label)
        self.items = widget_items

    def addItem(self, item):
        self.widget.addItem(item)

    def addItems(self, items):
        self.widget.add_items(items)


class ListWidgetItem(QtWidgets.QListWidgetItem):

    def __init__(self, text, tags=[]):
        super(ListWidgetItem, self).__init__(text=text)
        self.text = text
        self.widget_label = QtWidgets.QLabel(text)
        self.tags = tags

        # Case in-sensitive filtering
        self._text = text.lower()
        self._tags = [tag.lower() for tag in tags]

    def filter_by_text(self, text, include_tags=False):
        text = text.lower()

        if text in self._text:
            return True
        if include_tags:
            for tag in self._tags:
                if text in tag:
                    return True
        return False

    def get_value(self):
        return self.widget_label.text()

    def text(self):
        return self.get_value()



