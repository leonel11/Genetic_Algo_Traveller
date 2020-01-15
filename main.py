## @package main
# Основный модуль, с которого запускается программа

import sys

import GUIGeneticAlgo

from PyQt5.QtWidgets import *

# main function

app = QApplication(sys.argv)

mw = GUIGeneticAlgo.GuiGeneticAlgo()
mw.show()

sys.exit(app.exec_())