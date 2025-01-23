import maya.cmds as cmds
import pymel.core as pm
from functools import partial


# TODO: Should swap all pymel back to cmds where possible

# Node Types
#######################################

NODE_DICTIONARY = {
    'ADL': partial(pm.createNode, 'addDoubleLinear'),
    'blendROT': partial(pm.createNode, 'animBlendNodeAdditiveRotation'),
    'BLC': partial(pm.createNode, 'blendColors'),
    'BTA': partial(pm.createNode, 'blendTwoAttr'),
    'CFME': partial(pm.createNode, 'curveFromMeshEdge'),
    'CLMP': partial(pm.createNode, 'clamp'),
    'CMPM': partial(pm.createNode, 'composeMatrix'),
    'CND': partial(pm.createNode, 'condition'),
    'CPOS': partial(pm.createNode, 'closestPointOnSurface'),
    'curveInfo': partial(pm.createNode, 'curveInfo'),
    'DCPM': partial(pm.createNode, 'decomposeMatrix'),
    'DIST': partial(pm.createNode, 'distanceBetween'),
    '4x4M': partial(pm.createNode, 'fourByFourMatrix'),
    'INVM': partial(pm.createNode, 'inverseMatrix'),
    'LOFT': partial(pm.createNode, 'loft'),
    'MDIV': partial(pm.createNode, 'multiplyDivide'),
    'MDL': partial(pm.createNode, 'multDoubleLinear'),
    'MM': partial(pm.createNode, 'multMatrix'),
    'PMA': partial(pm.createNode, 'plusMinusAverage'),
    'PMM': partial(pm.createNode, 'pointMatrixMult'),
    'POCI': partial(pm.createNode, 'pointOnCurveInfo'),
    'POSI': partial(pm.createNode, 'pointOnSurfaceInfo'),
    'REV': partial(pm.createNode, 'reverse'),
    'RMPV': partial(pm.createNode, 'remapValue'),
    'SR': partial(pm.createNode, 'setRange'),
    'UC': partial(pm.createNode, 'unitConversion'),
    'VP': partial(pm.createNode, 'vectorProduct'),
    'WAM': partial(pm.createNode, 'wtAddMatrix')
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
    ft3_node = pm.createNode('unitConversion')
    pm.addAttr(ft3_node, longName='customInput', attributeType='double')
    pm.addAttr(ft3_node, longName='customOutput', attributeType='double3')
    pm.addAttr(ft3_node, longName='outX', attributeType='double', parent='customOutput')
    pm.addAttr(ft3_node, longName='outY', attributeType='double', parent='customOutput')
    pm.addAttr(ft3_node, longName='outZ', attributeType='double', parent='customOutput')

    pm.connectAttr(ft3_node + '.customInput', ft3_node + '.outX', force=True)
    pm.connectAttr(ft3_node + '.customInput', ft3_node + '.outY', force=True)
    pm.connectAttr(ft3_node + '.customInput', ft3_node + '.outZ', force=True)
    return ft3_node


NODE_DICTIONARY['FTT'] = float_to_three
