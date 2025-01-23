from PySide2 import QtWidgets, QtCore, QtGui


class WindowWidget(QtWidgets.QMainWindow):

	def pop_up_message(self, message):
		QtWidgets.QMessageBox.information(
			self,
			'Information',
			message,
			QtWidgets.QMessageBox.Ok)

	def pop_up_question(self, question):
		result = QtWidgets.QMessageBox.question(
			self,
			'Information',
			question,
			QtWidgets.QMessageBox.Yes,
			QtWidgets.QMessageBox.No)

		return result == QtWidgets.QMessageBox.Yes

	def pop_up_error(self, *error):
		errorText = ' '.join([str(e) for e in error])
		errorBox = QtWidgets.QMessageBox(
			QtWidgets.QMessageBox.Critical,
			'Error',
			errorText,
			buttons=QtGui.QMessageBox.Ok,
			parent=self,
			flags=QtCore.Qt.WindowStaysOnTopHint
		)
		errorBox.exec_()
		return errorBox

	# TODO: Not tested
	def custom_pop_up_message(self, **kwargs):
		custom_pop_up = CustomMessageBox(**kwargs)
		custom_pop_up.exec_()
		return custom_pop_up


class CustomMessageBox(QtWidgets.QDialog):

	def __init__(self, parent_instance, *args, **kwargs):
		super().__init__()
		self.parent_instance = parent_instance
		self.options = {}
		for k, v in kwargs.items():
			self.options[k] = v

		self.setModal(True)
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.setWindowTitle(self.window_name)
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

		self.setMinimumWidth(200)
		self.setMinimumHeight(200)

		self.setLayout(QtWidgets.QVBoxLayout())
		self.layout().setContentsMargins(1, 1, 1, 1)
		self.layout().setSpacing(5)

		self.base_widget = QtWidgets.QWidget()
		self.base_layout = QtWidgets.QVBoxLayout()
		self.base_widget.setLayout(self.base_layout)
		self.layout().addWidget(self.base_widget)

		self.build_ui()

	@classmethod
	def pop_up(cls, parent_instance, *args, **kwargs):
		pop_up = cls(parent_instance, *args, **kwargs)
		pop_up.exec_()
		return

	def build_ui(self):
		pass