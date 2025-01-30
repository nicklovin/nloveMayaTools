import maya.cmds as cmds
from functools import partial


# TODO: Should swap all pymel back to cmds where possible

# Node Types
#######################################

NODE_DICTIONARY = {
    'ADL': partial(cmds.createNode, 'addDoubleLinear'),
    'blendROT': partial(cmds.createNode, 'animBlendNodeAdditiveRotation'),
    'BLC': partial(cmds.createNode, 'blendColors'),
    'BTA': partial(cmds.createNode, 'blendTwoAttr'),
    'CFME': partial(cmds.createNode, 'curveFromMeshEdge'),
    'CLMP': partial(cmds.createNode, 'clamp'),
    'CMPM': partial(cmds.createNode, 'composeMatrix'),
    'CND': partial(cmds.createNode, 'condition'),
    'CPOS': partial(cmds.createNode, 'closestPointOnSurface'),
    'curveInfo': partial(cmds.createNode, 'curveInfo'),
    'DCPM': partial(cmds.createNode, 'decomposeMatrix'),
    'DIST': partial(cmds.createNode, 'distanceBetween'),
    '4x4M': partial(cmds.createNode, 'fourByFourMatrix'),
    'INVM': partial(cmds.createNode, 'inverseMatrix'),
    'LOFT': partial(cmds.createNode, 'loft'),
    'MDIV': partial(cmds.createNode, 'multiplyDivide'),
    'MDL': partial(cmds.createNode, 'multDoubleLinear'),
    'MM': partial(cmds.createNode, 'multMatrix'),
    'PMA': partial(cmds.createNode, 'plusMinusAverage'),
    'PMM': partial(cmds.createNode, 'pointMatrixMult'),
    'POCI': partial(cmds.createNode, 'pointOnCurveInfo'),
    'POSI': partial(cmds.createNode, 'pointOnSurfaceInfo'),
    'REV': partial(cmds.createNode, 'reverse'),
    'RMPV': partial(cmds.createNode, 'remapValue'),
    'SR': partial(cmds.createNode, 'setRange'),
    'UC': partial(cmds.createNode, 'unitConversion'),
    'VP': partial(cmds.createNode, 'vectorProduct'),
    'WAM': partial(cmds.createNode, 'wtAddMatrix')
}

ARK_NODE_DICTIONARY = {
    'FTV': 'FTV',
    'floatToVec': 'FTV',
    'ATV': 'ATV',
    'angleToVec': 'ATV',
    'VAC': 'VAC',
    'vectorAngleCone': 'VAC',
    'BDM': 'BDM',
    'breakdownMatrix': 'BDM',
}

NODE_NAME_DICTIONARY = {
    'addDoubleLinear': 'ADL',
    'ADL': 'ADL',
    'animBlendNodeAdditiveRotation': 'blendROT',
    'blendROT': 'blendROT',
    'blendColors': 'BLC',
    'BLC': 'BLC',
    'blendTwoAttr': 'BTA',
    'BTA': 'BTA',
    'clamp': 'CLMP',
    'CLMP': 'CLMP',
    'closestPointOnSurface': 'CPOS',
    'CPOS': 'CPOS',
    'condition': 'CND',
    'CND': 'CND',
    'curveFromMeshEdge': 'CFME',
    'CFME': 'CFME',
    'curveInfo': 'curveInfo',
    'composeMatrix': 'CMPM',
    'CMPM': 'CMPM',
    'decomposeMatrix': 'DCPM',
    'DCPM': 'DCPM',
    'distanceBetween': 'DIST',
    'DIST': 'DIST',
    'fourByFourMatrix': '4x4M',
    'FBFM': '4x4M',
    '4x4M': '4x4M',
    'floatTo3': 'FTT',
    'FTT': 'FTT',
    'inverseMatrix': 'INVM',
    'INVM': 'INVM',
    'loft': 'LOFT',
    'LOFT': 'LOFT',
    'multDoubleLinear': 'MDL',
    'MDL': 'MDL',
    'multiplyDivide': 'MDIV',
    'MDIV': 'MDIV',
    'multMatrix': 'MM',
    'MM': 'MM',
    'plusMinusAverage': 'PMA',
    'PMA': 'PMA',
    'pointMatrixMult': 'PMM',
    'PMM': 'PMM',
    'pointOnCurveInfo': 'POCI',
    'POCI': 'POCI',
    'pointOnSurfaceInfo': 'POSI',
    'POSI': 'POSI',
    'reverse': 'REV',
    'REV': 'REV',
    'remapValue': 'RMPV',
    'RMPV': 'RMPV',
    'setRange': 'SR',
    'SR': 'SR',
    'unitConversion': 'UC',
    'UC': 'UC',
    'vectorProduct': 'VP',
    'VECP': 'VP',
    'VP': 'VP',
    'wtAddMatrix': 'WAM',
    'WAM': 'WAM'
}

# TODO: This is leftover from studio setup.  Check if it has a purpose, remove if not.
# Plugin Types
#######################################

PLUGIN_LIBRARIES = {
    0: {
        'library': ARK_NODE_DICTIONARY,
        'prefix': '',
        'namespace': 'ARK'
    }
}

# Hierarchy Types
#######################################

DEFAULT_RIG_HIERARCHY = [
    'RigRootName', [
        'GLOBAL_MOVE', [
            'CTL',
            'IK',
            'JNT', [
                'BONE',
                'DRIVER'
            ]
        ],
        'GEO', [
            'ANIM_PROXY',
            'EXTRAS',
            'RENDER'
        ],
        'PLACEMENT', [
            'Global_CTL', [
                'Local_CTL'
            ]
        ],
        'MISC_NODES', [
            'DELETE_BEFORE_PUBLISH',
            'NODES_TO_HIDE',
            'NODES_TO_SHOW'
        ],
        'SCRIPT_NODES',
        'DEFORMER', [
            'BLENDSHAPES', [
                'LIVE_SHAPES',
                'RIBBONS',
                'SHAPES_TO_DELETE'
            ],
            'CUSTOM_SYSTEMS',
            'DEFORMER_HANDLE',
            'NONSCALE_JNTS'
        ],
    ]
]


# Custom nodes
def float_to_three():
    ft3_node = cmds.createNode('unitConversion')
    cmds.addAttr(ft3_node, longName='customInput', attributeType='double')
    cmds.addAttr(ft3_node, longName='customOutput', attributeType='double3')
    cmds.addAttr(ft3_node, longName='outX', attributeType='double', parent='customOutput')
    cmds.addAttr(ft3_node, longName='outY', attributeType='double', parent='customOutput')
    cmds.addAttr(ft3_node, longName='outZ', attributeType='double', parent='customOutput')

    cmds.connectAttr(ft3_node + '.customInput', ft3_node + '.outX', force=True)
    cmds.connectAttr(ft3_node + '.customInput', ft3_node + '.outY', force=True)
    cmds.connectAttr(ft3_node + '.customInput', ft3_node + '.outZ', force=True)
    return ft3_node


NODE_DICTIONARY['FTT'] = float_to_three
