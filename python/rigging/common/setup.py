from collections import OrderedDict

from PySide2 import QtWidgets, QtCore, QtGui

from ...widgets.common import frame
from ...basic import curve_builder
from ...basic import attributes
from ...basic import node_builder
from ...basic import utils
from ...decorators.undo import UndoBlock 

import maya.cmds as cmds

# reload(crv)
# reload(n)
# reload(nUtils)
# reload(tool)
# reload(frame)


def construct_hierarchy_dict():
    hierarchy_dict = OrderedDict()
    hierarchy_dict['GLOBAL_MOVE'] = {
        'IK': None,
        'CTL': None,
        'JNT': {
            'BONE': None,
            'DRIVER': None
        }
    }
    hierarchy_dict['GEO'] = {
        'EXTRAS': None,
        'ANIM_PROXY': None,
        'RENDER': None
    }
    hierarchy_dict['MISC_NODES'] = {
        'NODES_TO_SHOW': None,
        'NODES_TO_HIDE': None,
        'DELETE_BEFORE_PUBLISH': None
    }
    hierarchy_dict['PLACEMENT'] = {
        'Global_CTL': {
            'Local_CTL': None
        }
    }
    hierarchy_dict['SCRIPT_NODES'] = None
    hierarchy_dict['DEFORMER'] = {
        'BLENDSHAPES': {
            'RIBBONS': None,
            'LIVE_SHAPES': None,
            'SHAPES_TO_DELETE': None
        },
        'NONSCALE_JNTS': None,
        'CUSTOM_SYSTEMS': None,
        'DEFORMER_HANDLE': None
    }
    return hierarchy_dict


def simple_rig_setup(rig_name):
    hierarchy_dict = construct_hierarchy_dict()

    root_node = cmds.createNode('transform', name=rig_name)
    base_children = []
    for base, sub_one in hierarchy_dict.items():
        base_node = utils.create_null(name=base, suffix='GRP')
        if sub_one:
            sub_one_children = []
            for one, sub_two in sub_one.items():
                sub_one_node = utils.create_null(name=one, suffix='GRP')
                if sub_two:
                    sub_two_children = []
                    for two, sub_three in sub_two.items():
                        sub_two_node = utils.create_null(name=two, suffix='GRP')
                        sub_two_children.append(sub_two_node)
                    cmds.parent(sub_two_children, sub_one_node)
                sub_one_children.append(sub_one_node)
            cmds.parent(sub_one_children, base_node)
        base_children.append(base_node)
    cmds.parent(base_children, root_node)

    cmds.rename('Local_CTL_GRP', 'Local_CTL')
    cmds.rename('Global_CTL_GRP', 'Global_CTL')

    curve_builder.add_curve_shape('rounded_square', transform_node='Local_CTL', color='orange')
    curve_builder.add_curve_shape('master_move', transform_node='Global_CTL', color='yellow')

    # connecting global move parts to the matrix of the master controllers
    global_matrix = node_builder.create_node('DCPM', name='GLOBAL')
    cmds.connectAttr('Local_CTL.worldMatrix',
                     global_matrix + '.inputMatrix')
    cmds.connectAttr(global_matrix + '.outputTranslate',
                     'GLOBAL_MOVE_GRP.translate')
    cmds.connectAttr(global_matrix + '.outputRotate', 'GLOBAL_MOVE_GRP.rotate')
    cmds.connectAttr(global_matrix + '.outputScale', 'GLOBAL_MOVE_GRP.scale')
    # set geo grp to reference by default
    cmds.setAttr('GEO_GRP.overrideEnabled', 1)
    cmds.setAttr('GEO_GRP.overrideDisplayType', 2)

    # add attrs to global and local + set connections
    attributes.create_attr(
        attribute_name='localScale',
        attribute_type='double',
        input_object='Local_CTL',
        default_value=1,
        min_value=0.01)
    attributes.create_attr(
        attribute_name='globalScale',
        attribute_type='double',
        input_object='Global_CTL',
        default_value=1,
        min_value=0.01)
    attributes.create_attr(
        attribute_name='GEO',
        attribute_type='enum',
        input_object='Global_CTL',
        enum_names=['-------'],
        keyable=False,
        channelbox=True)
    attributes.create_attr(
        attribute_name='geoSelectable',
        attribute_type='enum',
        input_object='Global_CTL',
        enum_names=['Normal', 'Template', 'Reference'],
        keyable=False,
        channelbox=True)
    attributes.create_attr(
        attribute_name='geoVis',
        attribute_type='enum',
        input_object='Global_CTL',
        enum_names=['Proxy', 'Render'],
        keyable=False,
        channelbox=True)

    # Geo Selectable connections
    cmds.connectAttr('Global_CTL.geoSelectable', 'GEO_GRP.overrideDisplayType')

    # Geo Vis connections
    reverse_vis = node_builder.create_node('REV', name='Global_geoVis')
    cmds.connectAttr('Global_CTL.geoVis', 'RENDER_GRP.visibility')
    cmds.connectAttr('Global_CTL.geoVis', reverse_vis + '.inputX')
    cmds.connectAttr(reverse_vis + '.outputX', 'ANIM_PROXY_GRP.visibility')

    for s in ['X', 'Y', 'Z']:
        cmds.connectAttr('Local_CTL' + '.localScale',
                         'Local_CTL' + '.scale' + s)
        cmds.connectAttr('Global_CTL' + '.globalScale',
                         'Global_CTL' + '.scale' + s)

    attributes.lock_attrs(
        nodes=['Local_CTL', 'Global_CTL'],
        attrs=['sx', 'sy', 'sz', 'v'],
        hide=True)

    # TODO: What is this returning for?
    return 'Global_CTL', 'Local_CTL'


class CreateRigWidget(frame.MayaFrameWidget):

    def __init__(self):
        QtWidgets.QFrame.__init__(self)

        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)

        create_rig_widget = QtWidgets.QWidget()
        create_rig_widget.setLayout(QtWidgets.QVBoxLayout())
        create_rig_widget.layout().setContentsMargins(2, 2, 2, 2)
        create_rig_widget.layout().setSpacing(5)
        create_rig_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                        QtWidgets.QSizePolicy.Fixed)
        self.layout().addWidget(create_rig_widget)

        name_layout = QtWidgets.QHBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        create_rig_widget.layout().addLayout(name_layout)
        create_rig_widget.layout().addLayout(button_layout)

        # Input Name ----------------------------------------------- #
        name_label = QtWidgets.QLabel('Rig Name:')
        self.name_line_edit = QtWidgets.QLineEdit()

        reg_ex = QtCore.QRegExp('^(?!@$^_)[a-zA-Z_0-9]+')
        text_validator = QtGui.QRegExpValidator(reg_ex,
                                                self.name_line_edit)
        self.name_line_edit.setValidator(text_validator)

        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_line_edit)

        # Buttons -------------------------------------------------- #
        self.create_rig_button = QtWidgets.QPushButton('Create Rig')
        button_layout.addWidget(self.create_rig_button)

        # Connections ---------------------------------------------- #
        self.create_rig_button.clicked.connect(self.create_rig)

    def create_rig(self):
        name = str(self.name_line_edit.text()).strip()
        if not name:
            return self.popUpError(ValueError('Invalid input for Rig Name!'))

        with UndoBlock():
            simple_rig_setup(name)
