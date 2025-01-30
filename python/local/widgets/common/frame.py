from PySide2 import QtWidgets, QtCore, QtGui


class MayaFrameWidget(QtWidgets.QFrame):

	def popUpMessage(self, message):
		QtWidgets.QMessageBox.information(
			self,
			'Information',
			message,
			QtWidgets.QMessageBox.Ok)

	def popUpQuestion(self, question):
		result = QtWidgets.QMessageBox.question(
			self,
			'Information',
			question,
			QtWidgets.QMessageBox.Yes,
			QtWidgets.QMessageBox.No)

		return result == QtWidgets.QMessageBox.Yes

	def popUpError(self, *error):
		error_text = ' '.join([str(e) for e in error])
		error_box = QtWidgets.QMessageBox(
			QtWidgets.QMessageBox.Critical,
			'Error',
			error_text,
			buttons=QtWidgets.QMessageBox.Ok,
			parent=self,
			flags=QtCore.Qt.WindowStaysOnTopHint
		)
		error_box.exec_()
		return error_box
