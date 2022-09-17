from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QMetaObject
from config import WORK_DIRECTORY

def loadUi(ui_file,parent):
	loader = UiLoader(parent)
	loader.setWorkingDirectory(WORK_DIRECTORY)
	widget = loader.load(ui_file)
	QMetaObject.connectSlotsByName(widget)
	return widget

class UiLoader(QUiLoader):
	"""
	Subclass :class:`~PySide.QtUiTools.QUiLoader` to create the user interface
	in a base instance.
	Unlike :class:`~PySide.QtUiTools.QUiLoader` itself this class does not
	create a new instance of the top-level widget, but creates the user
	interface in an existing instance of the top-level class.
	This mimics the behaviour of :func:`PyQt4.uic.loadUi`.
	"""

	def __init__(self, baseinstance, customWidgets=None):
		"""
		Create a loader for the given ``baseinstance``.
		The user interface is created in ``baseinstance``, which must be an
		instance of the top-level class in the user interface to load, or a
		subclass thereof.
		``customWidgets`` is a dictionary mapping from class name to class object
		for widgets that you've promoted in the Qt Designer interface. Usually,
		this should be done by calling registerCustomWidget on the QUiLoader, but
		with PySide 1.1.2 on Ubuntu 12.04 x86_64 this causes a segfault.
		``parent`` is the parent object of this loader.
		"""

		QUiLoader.__init__(self, baseinstance)
		self.baseinstance = baseinstance
		self.customWidgets = customWidgets

	def createWidget(self, class_name, parent=None, name=''):
		"""
		Function that is called for each widget defined in ui file,
		overridden here to populate baseinstance instead.
		"""

		if parent is None and self.baseinstance:
			# supposed to create the top-level widget, return the base instance
			# instead
			return self.baseinstance

		else:
			if class_name in self.availableWidgets():
				# create a new widget for child widgets
				widget = QUiLoader.createWidget(self, class_name, parent, name)

			else:
				# if not in the list of availableWidgets, must be a custom widget
				# this will raise KeyError if the user has not supplied the
				# relevant class_name in the dictionary, or TypeError, if
				# customWidgets is None
				try:
					widget = self.customWidgets[class_name](parent)

				except (TypeError, KeyError) as e:
					raise Exception('No custom widget ' + class_name + ' found in customWidgets param of UiLoader __init__.')

			if self.baseinstance:
				# set an attribute for the new child widget on the base
				# instance, just like PyQt4.uic.loadUi does.
				setattr(self.baseinstance, name, widget)

				# this outputs the various widget names, e.g.
				# sampleGraphicsView, dockWidget, samplesTableView etc.
				#print(name)

			return widget
