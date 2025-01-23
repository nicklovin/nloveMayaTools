from PySide2 import QtWidgets, QtCore, QtGui

from ..common.splitter import Splitter

import maya.mel as mel
import maya.cmds as cmds
import pymel.core as pm


class GlobalToolWidget(QtWidgets.QFrame):

    def __init__(self):
        QtWidgets.QFrame.__init__(self)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)

        global_widget = QtWidgets.QWidget()
        global_widget.setLayout(QtWidgets.QVBoxLayout())
        global_widget.layout().setContentsMargins(2, 2, 2, 2)
        global_widget.layout().setSpacing(5)
        global_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                    QtWidgets.QSizePolicy.Fixed)

        publish_widget = QtWidgets.QWidget()
        publish_widget.setLayout(QtWidgets.QVBoxLayout())
        publish_widget.layout().setContentsMargins(2, 2, 2, 2)
        publish_widget.layout().setSpacing(5)
        publish_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                     QtWidgets.QSizePolicy.Fixed)

        self.layout().addWidget(global_widget)
        self.layout().addWidget(Splitter('Rig Mode'))
        self.layout().addWidget(publish_widget)

        # Layouts
        button_layout = QtWidgets.QHBoxLayout()
        publish_layout = QtWidgets.QHBoxLayout()

        # Add layouts to widget
        global_widget.layout().addLayout(button_layout)
        publish_widget.layout().addLayout(publish_layout)

        # Buttons
        self.flip_selection_button = QtWidgets.QPushButton('Flip Selection')
        self.add_iso_button = QtWidgets.QPushButton('Add to Isolate View')
        self.remove_iso_button = QtWidgets.QPushButton('Remove from Isolate View')

        button_layout.addWidget(self.flip_selection_button)
        button_layout.addWidget(self.add_iso_button)
        button_layout.addWidget(self.remove_iso_button)

        self.publish_mode_button = QtWidgets.QPushButton('Publish Mode')
        self.edit_mode_button = QtWidgets.QPushButton('Edit Mode')

        publish_layout.addWidget(self.publish_mode_button)
        publish_layout.addWidget(self.edit_mode_button)

        self.flip_selection_button.clicked.connect(self.flip_selection)
        self.add_iso_button.clicked.connect(self.add_to_isolate)
        self.remove_iso_button.clicked.connect(self.remove_from_isolate)

        # self.publish_mode_button.clicked.connect(self.publish_mode)
        # self.edit_mode_button.clicked.connect(self.edit_mode)

    def flip_selection(self):
        sel = cmds.ls(selection=True, recursive=True)
        flip = []

        namespace = None
        if ':' in sel[0]:
            sel = [obj.split(':')[1] for obj in sel]
            namespace = sel[0].split(':')[0]

        for item in sel:
            if '_L_' in item:
                flip.append(item.replace('_L_', '_R_'))
            elif '_R_' in item:
                flip.append(item.replace('_R_', '_L_'))
            elif item.startswith('R_'):
                flip.append('L_' + item[2:])
            elif item.startswith('L_'):
                flip.append('R_' + item[2:])
            elif item.endswith('_R'):
                flip.append(item[:-2] + '_L')
            elif item.endswith('_L'):
                flip.append(item[:-2] + '_R')
            else:
                cmds.warning('Nothing done.')

        if namespace:
            flip = [':'.join([namespace, item]) for item in flip]

        cmds.select(flip, replace=True)

    def add_to_isolate(self):
        mel.eval('isolateSelect -addSelected modelPanel4;')

    def remove_from_isolate(self):
        mel.eval('isolateSelect -removeSelected modelPanel4;')

    def publish_mode(self):
        pass

    def edit_mode(self):
        pass
