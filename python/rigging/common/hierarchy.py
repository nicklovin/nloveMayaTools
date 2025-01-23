# from collections import OrderedDict

from PySide2 import QtWidgets, QtCore, QtGui

from ...constants import node_blueprints

import maya.cmds as cmds


class Hierarchy(object):
    """
    Example Hiearchy:
    [
        'RigRootName', [
            'GLOBAL_MOVE', [
                'CTL',
                'IK',
                'JNT', [
                    'BONE',
                    'DRIVER'
                ]
            ]
        ]
    ]
    """

    defaultHierarchy = node_blueprints.DEFAULT_RIG_HIERARCHY[:]

    def __init__(self, hierarchy, value_type='string'):
        self.hierarchy = hierarchy
        self.objectHierarchy = []

        if value_type == 'string':
            self.create_hierarchy()
        elif value_type == 'object':
            self.create_object_hierarchy()

    def recurse_build(self, contents, parent_node):
        latest_node = None
        for node in contents:
            if isinstance(node, str):
                latest_node = cmds.createNode('transform', name=node)
                if parent_node is not None:
                    cmds.parent(node, parent_node)
            elif isinstance(node, (list, tuple)):
                self.recurse_build(node, latest_node)
            elif isinstance(node, dict):
                node_tuples = node.items()
                for nodeTuple in node_tuples:
                    self.recurse_build(nodeTuple, latest_node)

    def recurse_object_build(self, contents, parent_node):
        latest_node = None
        row = []
        for node in contents:
            if isinstance(node, str):
                latest_node = TransformNode(name=node)
                if parent_node is not None:
                    latest_node._parent = parent_node
                row.append(latest_node)
            elif isinstance(node, (list, tuple)):
                children = self.recurse_object_build(node, latest_node)
                latest_node._children = children
        return row

    def create_hierarchy(self):
        """
        Builds the hierarchy based on input

        - if self.hierarchy is a list type, recurse_build will run normally
        - if self.hierarchy is a string, presume rig hierarchy and use input as the root node name
        - if self.hierarchy is a dict, runs similar to list but messier and does not maintain order

        """
        if isinstance(self.hierarchy, (list, tuple)):
            self.recurse_build(self.hierarchy, None)
        elif isinstance(self.hierarchy, str):
            # Copy default rig hierarchy
            contents = self.defaultHierarchy
            contents[0] = self.hierarchy
            self.recurse_build(contents, None)
        elif isinstance(self.hierarchy, dict):
            contents = self.hierarchy.items()
            self.recurse_build(contents, None)

    def create_object_hierarchy(self):
        tree = self.recurse_object_build(self.hierarchy, None)
        self.objectHierarchy = tree


class TransformNode(object):

    def __init__(self, name='', parent=None):
        self._parent = parent
        self._name = name
        self._children = []

    def children(self):
        return self._children

    def parent(self):
        return self._parent

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def insert_child(self, position, child):
        if 0 <= position < len(self._children):
            self._children.insert(position, child)
            child._parent = self
            return True
        return False

    def remove_child(self, position):
        if 0 <= position < len(self._children):
            child = self._children.pop(position)
            child._parent = None
            return True
        return False

    def get_child_by_index(self, index):
        if 0 <= index < len(self._children):
            return self._children[index]
        else:
            raise IndexError('Invalid index!')

    def get_child_by_name(self, name):
        for child in self._children:
            if child.name() == name:
                return child
        return None


class HierarchyTreeWidget(QtWidgets.QFrame):

    # Should have a dropdown of defaults/saved hierarchy builds
    defaultTree = Hierarchy(hierarchy=node_blueprints.DEFAULT_RIG_HIERARCHY, value_type='object')

    def __init__(self):
        QtWidgets.QFrame.__init__(self)

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(1, 1, 1, 1)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignTop)

        hierarchy_widget = QtWidgets.QWidget()
        hierarchy_widget.setLayout(QtWidgets.QVBoxLayout())
        hierarchy_widget.layout().setContentsMargins(2, 2, 2, 2)
        hierarchy_widget.layout().setSpacing(5)
        hierarchy_widget.setSizePolicy(QtWidgets.QSizePolicy.Minimum,
                                       QtWidgets.QSizePolicy.Fixed)
        self.layout().addWidget(hierarchy_widget)

        tree_layout = QtWidgets.QHBoxLayout()

        hierarchy_widget.layout().addLayout(tree_layout)

        # ---------------
        self.treeData = {}

        # ---------------
        self.tree_widget = QtWidgets.QTreeView()
        model = QtGui.QStandardItemModel()
        self.tree_widget.setModel(model)
        self.rootItem = model.invisibleRootItem()

        self.addFromTree(self.defaultTree.objectHierarchy)
        tree_layout.addWidget(self.tree_widget)

        self.tree_widget.expandAll()

    def addItem(self, item, parent=''):
        tree_item = QtGui.QStandardItem(item.name())
        # tree_item.setData(item)
        if parent:
            parent_item = self.treeData[parent]
            parent_item.appendRow(tree_item)
        else:
            self.rootItem.appendRow(tree_item)
            self.treeData[item.name()] = tree_item

    def addChildrenFromTree(self, parent, children):
        for child in children:
            tree_item = QtGui.QStandardItem(child.name())
            parent.appendRow(tree_item)
            if child.children():
                self.addChildrenFromTree(tree_item, child.children())

    def addFromTree(self, tree):
        root = tree[0]
        tree_item = QtGui.QStandardItem(root.name())
        children = root.children()

        self.rootItem.appendRow(tree_item)
        self.addChildrenFromTree(tree_item, children)
