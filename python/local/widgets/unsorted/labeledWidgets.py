from functools import partial
from PySide2 import QtWidgets, QtCore, QtGui

# TODO: Be aware that this will definitely need to be refactored later
from local.widgets.unsorted import dynamicListWidgets as dyWidgets


class LabelLineEdit(QtWidgets.QWidget):

    def __init__(
            self,
            title,
            default_text='',
            placeholder_text='',
            regex='',
            width=None,
            *args,
            **kwargs):

        super(LabelLineEdit, self).__init__(*args, **kwargs)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        # self.text = title
        self.label = QtWidgets.QLabel(title)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label.setMaximumHeight(100)
        self.label.setFixedWidth(width if width else 100)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        # self.label.set

        self.line_edit = QtWidgets.QLineEdit(default_text)
        if placeholder_text:
            self.line_edit.setPlaceholderText(placeholder_text)
        if regex:
            self._set_regex(regex)
        self.line_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        # self.layout.addSpacerItem(
        #     QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # )
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.line_edit)
        self.setLayout(self.layout)

    def _set_regex(self, regex_string=''):
        reg = QtCore.QRegExp(regex_string)
        text_validator = QtGui.QRegExpValidator(reg, self.line_edit)
        self.line_edit.setValidator(text_validator)

    def get_value(self):
        return self.line_edit.text()

    def set_value(self, text):
        self.line_edit.setText(str(text))

    # Wrapped widget re-directs
    def clear(self):
        self.line_edit.clear()

    def text(self):
        return self.get_value()


class LabelNumberEdit(LabelLineEdit):

    money_regex = '|'.join([
        r'^\$?(\d*\.\d{1,2})$',  # e.g., $.50, .50, $1.50, $.5, .5
        r'^\$?(\d+)$',  # e.g., $500, $5, 500, 5
        r'^\$(\d+\.?)$',  # e.g., $5.
    ])
    int_regex = r'\d*'
    float_regex = r'^\d*(\.\d*)$'

    def __init__(
            self,
            title,
            default_text='',
            placeholder_text='',
            regex='',
            width=None,
            *args,
            **kwargs):
        super(LabelNumberEdit, self).__init__(
                title, default_text, placeholder_text, regex='', width=width, *args, **kwargs)
        self.regex_type = regex
        if regex == 'float':
            regex_string = self.float_regex
        elif regex == 'int':
            regex_string = self.int_regex
        elif regex == 'money':
            regex_string = self.money_regex
        elif not regex:
            raise AttributeError(
                    'Invalid input given for argument "regex="!  '
                    'Must be in ("int", "float", "money") or custom written.')
        else:
            regex_string = regex

        self._set_regex(regex_string)

    def get_value(self):
        if self.regex_type == 'float':
            return float(self.line_edit.text())
        elif self.regex_type == 'int':
            return int(self.line_edit.text())
        else:
            return self.get_text()

    def get_text(self):
        return super(LabelNumberEdit, self).get_value()


class LabelParagraphBox(QtWidgets.QWidget):

    def __init__(
            self,
            title,
            default_text='',
            placeholder_text='paragraph format...',
            regex='',
            width=None,
            *args,
            **kwargs):

        super(LabelParagraphBox, self).__init__(*args, **kwargs)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.text = title
        self.label = QtWidgets.QLabel(title)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label.setMaximumHeight(100)
        self.label.setFixedWidth(width if width else 100)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        # self.label.set

        self.text_edit = QtWidgets.QTextEdit(default_text)
        if placeholder_text:
            self.text_edit.setPlaceholderText(placeholder_text)
        if regex:
            reg = QtCore.QRegExp(regex)
            text_validator = QtGui.QRegExpValidator(reg, self.text_edit)
            self.text_edit.setValidator(text_validator)
        self.text_edit.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        # self.layout.addSpacerItem(
        #     QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # )
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_edit)
        self.setLayout(self.layout)

    def get_value(self):
        return self.text_edit.toPlainText()

    def clear(self):
        self.text_edit.clear()


class LabelComboBox(QtWidgets.QWidget):

    def __init__(self, title, items=[], width=None, *args, **kwargs):
        super(LabelComboBox, self).__init__(*args, **kwargs)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        # self.text = title
        self.label = QtWidgets.QLabel(title)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label.setMaximumHeight(100)
        self.label.setFixedWidth(width if width else 100)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.combo_box = QtWidgets.QComboBox()
        self.combo_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                     QtWidgets.QSizePolicy.Expanding)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo_box)
        self.setLayout(self.layout)

    # Re-creating methods to match the Qt objects
    def addItems(self, items):
        self.combo_box.addItems(items)

    def addItem(self, icon, item):
        if isinstance(icon, str):
            raise AttributeError('First argument in QComboBox.addItem expects QIcon or None.')
        self.combo_box.addItem(icon, item)

    def get_value(self):
        return self.combo_box.currentText()

    def set_value(self, value):
        if isinstance(value, int):
            self.setCurrentIndex(value)
        else:
            self.setCurrentText(value)

    def setCurrentText(self, text):
        self.combo_box.setCurrentText(text)

    def setCurrentIndex(self, index):
        self.combo_box.setCurrentIndex(index)


class LabelList(QtWidgets.QWidget):
    pass


class LabelDynamicList(QtWidgets.QWidget):

    def __init__(self, title, input_type='text', input_options=[], width=None, *args, **kwargs):
        super(LabelDynamicList, self).__init__(*args, **kwargs)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        # self.text = title
        self.label = QtWidgets.QLabel(title)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label.setMaximumHeight(100)
        self.label.setFixedWidth(width if width else 100)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.dynamic_list = dyWidgets.DynamicListWidget(
                title, input_type=input_type, input_options=input_options)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.setSpacing(1)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.dynamic_list)
        self.setLayout(self.layout)

    def delete_button(self, sender):
        return self.dynamic_list.delete_button(sender)

    def add_item(self):
        print(self)
        return self.dynamic_list.add_item()

    def get_values(self):
        return [item.get_value() for item in self.get_items()]

    def current_value(self):
        return self.dynamic_list.current_value()

    def current_item_changed(self):
        return self.dynamic_list.current_item_changed()

    def get_selected_item(self):
        return self.current_value()

    def get_items(self):
        return self.dynamic_list.get_items()

    def clear(self):
        self.dynamic_list.clear()


class LabelRadioButtons(QtWidgets.QWidget):

    radio_buttons = {}

    def __init__(self, title, items=[], width=None, height=None, default='', *args, **kwargs):
        super(LabelRadioButtons, self).__init__(*args, **kwargs)

        self.items = items
        self.default = default
        self.value = default

        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # self.text = title
        self.label = QtWidgets.QLabel(title)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.label.setMaximumHeight(100)
        self.label.setFixedWidth(width if width else 100)
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        # self.combo_box = QtWidgets.QComboBox()
        # self.combo_box.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
        #                              QtWidgets.QSizePolicy.Expanding)
        self.create_radio_buttons()

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.setContentsMargins(1, 1, 1, 1)
        self.layout.addWidget(self.label)
        for radio in self.items:
            self.layout.addWidget(self.radio_buttons[radio])

        self.setFixedHeight(width if width else 100)
        self.setLayout(self.layout)

    def _value_changed(self, button):
        # Safety check
        if self.radio_buttons[button].isChecked() is True:
            self.value = button
        else:
            raise ValueError('Value change not correctly set!')

        print(self.value)

    def create_radio_buttons(self):
        for radio in self.items:
            radio_button = QtWidgets.QRadioButton(radio)
            if self.default == radio:
                radio_button.setChecked(True)
            else:
                radio_button.setChecked(False)
            self.radio_buttons[radio] = radio_button
            radio_button.clicked.connect(partial(self._value_changed, radio_button.text()))

    def get_value(self):
        return self.value