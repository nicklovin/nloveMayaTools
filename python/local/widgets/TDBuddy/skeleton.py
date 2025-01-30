from PySide2 import QtWidgets, QtGui, QtCore
from functools import partial

from local.widgets.common.splitter import Splitter, SplitterLayout
from local.widgets.common.button import ShelfButton

import maya.mel as mel
import maya.cmds as cmds


class SkeletonToolsWidget(QtWidgets.QWidget):

    current_tool_context = None

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                           QtWidgets.QSizePolicy.Fixed)

        try:
            style_sheet_file = open(r'/stylesheets/shelf button scheme.qss', 'r')
            self.setStyleSheet(style_sheet_file.read())
        except IOError:
            pass

        self.setLayout(QtWidgets.QVBoxLayout())

        basic_joint_widget = QtWidgets.QWidget()
        basic_joint_widget.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(basic_joint_widget)

        basic_joint_widget.layout().addWidget(Splitter('Joints'))

        # Button Layouts
        joint_button_layout = QtWidgets.QHBoxLayout()
        ik_button_layout = QtWidgets.QHBoxLayout()
        custom_script_layout = QtWidgets.QHBoxLayout()

        basic_joint_widget.layout().addLayout(joint_button_layout)

        joint_icon = QtGui.QIcon(':/kinJoint.png')
        joint_button = ShelfButton(joint_icon)

        insert_joint_button = ShelfButton()

        mirror_joint_button = ShelfButton()

        locator_button = ShelfButton()

        orient_joint_button = ShelfButton()

        joint_button_layout.addWidget(joint_button)
        joint_button_layout.addWidget(insert_joint_button)
        joint_button_layout.addWidget(mirror_joint_button)
        joint_button_layout.addWidget(locator_button)
        joint_button_layout.addWidget(orient_joint_button)

        self.layout().addLayout(SplitterLayout())
        
        basic_ik_widget = QtWidgets.QWidget()
        basic_ik_widget.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(basic_ik_widget)

        basic_ik_widget.layout().addWidget(Splitter('IK'))

        basic_ik_widget.layout().addLayout(ik_button_layout)

        ik_handle_button = ShelfButton()

        ik_spline_button = ShelfButton()

        ribbon_button = ShelfButton()

        ik_button_layout.addWidget(ik_handle_button)
        ik_button_layout.addWidget(ik_spline_button)
        ik_button_layout.addWidget(ribbon_button)

        self.layout().addLayout(SplitterLayout())

        custom_script_widget = QtWidgets.QWidget()
        custom_script_widget.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(custom_script_widget)

        custom_script_widget.layout().addWidget(
            Splitter('Custom Tools'))
        custom_script_widget.layout().addLayout(custom_script_layout)

        create_pivot_button = ShelfButton()

        custom_script_layout.addWidget(create_pivot_button)

        joint_button.clicked.connect(self.joint_tool_context)

    @staticmethod
    def set_context_index(context_string):
        index = 1
        context_name = ''
        context_condition = True
        while context_condition is True:
            context_name = context_string + str(index)
            context_condition = cmds.contextInfo(context_name, exists=True)
            index += 1

            if index > 100:
                print('infinite loop... stopping')
                return

        return context_name

    def joint_tool_context(self):
        if cmds.currentCtx() == self.current_tool_context:
            return

        context_string = self.set_context_index('jointContext')

        cmds.jointCtx(context_string)
        cmds.setToolTo(context_string)
        self.current_tool_context = context_string
        print('Context set to %s' % context_string)

    def insert_joint_context(self):
        pass

    def mirror_joints(self):
        # May not be needed
        pass

    def orient_joints(self):
        # Probably trashed later
        pass

    def insert_joint_group(self, joint_count):
        # insert joints evenly between two selected joints
        # joint count determined by a slider
        pass

    def ik_handle_context(self, chain_type):
        pass

    def ik_spline_context(self):
        pass

    def ribbon_builder(self):
        # Will need to import ribbon script and use previous params
        pass

    def create_pivot(self):
        pass
