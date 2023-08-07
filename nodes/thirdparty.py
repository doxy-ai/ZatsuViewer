import sys
import os

sys.path.append(os.path.join(os.getcwd(), "../thirdparty/python-node-editor"))

from node_editor import *
from colour import Color
from PySide6 import QtGui

def color2QT(c: Color):
	return QtGui.QColor(c.red * 255, c.green * 255, c.blue * 255)