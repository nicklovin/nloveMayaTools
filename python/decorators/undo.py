import pymel.core as pymel


class UndoBlock(object):
	def __enter__(self, *args, **kwargs):
		pymel.undoInfo(openChunk=True)

	def __exit__(self, *args, **kwargs):
		pymel.undoInfo(closeChunk=True)

# TODO: Repeatable Context
