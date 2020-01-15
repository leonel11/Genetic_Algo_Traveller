## @package GUIGeneticAlgo
# Модуль для работы с графическим окном приложения

import os
import time

import Graph
import GeneticAlgo

from PyQt5.QtWidgets import *
from PyQt5 import uic

from Enums import StartPopulation, NewPopulation, MutationType

# Константы модуля
MAX_HROMOSOMES = 9999

## @class GUIGeneticAlgo
class GuiGeneticAlgo(QDialog):

    ## Конструктор
    def __init__(self):
        QDialog.__init__(self)
        uic.loadUi('GeneticAlgoDialog.ui', self) # установление связи с ui-файлом окна приложения
        # установка связи слотов с сигналами
        self.GraphButton.clicked.connect(self.OpenGraphFile)
        self.FindButton.clicked.connect(self.FindQuickestWay)
        self.SaveButton.clicked.connect(self.SaveResults)
        self.__filepath = ''
        self.__bestway = []

    ## Слот, осуществляющий открытие файла с графом
    def OpenGraphFile(self):
        default_readdir = os.getcwd() # текущая директория приложения
        # запуск стандартного окна открытия файла
        file_name = QFileDialog.getOpenFileName(self, 'Считать данные из файла', default_readdir, '*.txt', )[0]
        if file_name:
            self.__filepath = file_name
            self.GraphLineEdit.setText(self.__filepath)
            self.__graph = Graph.Graph(self.__filepath)
            self.SetHromosomeCountLimit(self.__graph.GetAllDifferentWaysCount())
            self.ClearResults()
        else:
            self.SetHromosome('')

    ## Слот, осуществляющий поиск кратчайшего пути с помощью генетического алгоритма
    def FindQuickestWay(self):
        if self.__filepath:
            genalgo = GeneticAlgo.GeneticAlgo(self.__graph, float(self.TournamentSpinBox.value()) / 100.0,
                                              self.GetMutationType(), float(self.MutationSpinBox.value()) / 100.0,
                                              int(self.IterationSpinBox.value()), int(self.HromosomeSpinBox.value()),
                                              self.GetStartPopulationType(), self.GetNewPopulationType())
            self.__bestway = genalgo.FindQuickestWay()
            if self.__bestway: # отображение результатов о кратчайшем пути
                strtime = time.strftime("%H:%M", time.gmtime(genalgo.GetHromosomeWayTime(self.__bestway)))
                strlen = str(genalgo.GetHromosomeWayLength(self.__bestway))
                self.SetHromosome(str(self.__bestway))
                self.SetHromosomeValues(strtime, strlen)
            else:
                self.SetHromosome('[ ]')
        else:
            self.SetHromosome('Пожалуйста, загрузите файл с описанием графа!')

    ## Отображение кратчайшего пути
    # @param hromosome - кратчайший путь
    def SetHromosome(self, bestway):
        self.ResultsLineEdit.setText(bestway)

    ## Отображение времени и длины кратчайшего пути
    def SetHromosomeValues(self, strtime, strlen):
        self.TimeLineEdit.setText(strtime)
        self.LengthLineEdit.setText(strlen)

    ## Очистка виджетов для отображения информации о кратчайшем пути
    def ClearResults(self):
        self.ResultsLineEdit.setText('')
        self.TimeLineEdit.setText('')
        self.LengthLineEdit.setText('')

    ## Слот, осуществляющий сохранение результатов о кратчайшем пути в графе
    def SaveResults(self):
        if not self.__filepath:
            self.SetHromosome('Для начала выполните поиск кратчайшего пути!')
        else:
            file_name = QFileDialog.getSaveFileName(self, 'Сохранить данные в файл', os.getcwd() + '/results', '*.txt')[0]
            if file_name:
                self.SaveData(file_name)

    ## Сохранение данных о кратчайшем пути
    # @param filename - путь до файла для сохранения нужной информации
    def SaveData(self, filename):
        f = open(filename, 'w')
        f.write('Наилучшая хромосома: ' + str(self.ResultsLineEdit.text()) + '\n')
        f.write('Время пути: ' + str(self.TimeLineEdit.text()) + '\n')
        f.write('Длина пути: ' + str(self.LengthLineEdit.text()))
        f.close()

    ## Установка ограничения на максимально возможное количество хромосом в начальной популяции
    # @param countlimit - количество всевозможных путей
    def SetHromosomeCountLimit(self, countlimit):
        if countlimit <= MAX_HROMOSOMES:
            self.HromosomeSpinBox.setMaximum(countlimit)
            if (self.HromosomeSpinBox.value() > countlimit):
                self.HromosomeSpinBox.setValue(countlimit)
        else:
            self.HromosomeSpinBox.setMaximum(MAX_HROMOSOMES)

    ## Функция, возвращающая способ формирования начальной популяции для генетического алгоритма
    def GetStartPopulationType(self):
        if self.EliteRadioButton.isChecked():
            return StartPopulation.ELITE
        if self.FullRadioButton.isChecked():
            return StartPopulation.FULL
        return StartPopulation.ELITE

    ## Функция, возвращающая способ формирования новой популяции для генетического алгоритма
    def GetNewPopulationType(self):
        if self.ClassicRadioButton.isChecked():
            return NewPopulation.CLASSIC
        if self.GenitorRadioButton.isChecked():
            return NewPopulation.GENITOR
        return NewPopulation.CLASSIC

    ## Функция, возвращающая вид мутации
    def GetMutationType(self):
        if self.OnePointRadioButton.isChecked():
            return MutationType.ONEPOINT
        if self.ManyPointsRadioButton.isChecked():
            return MutationType.MULTIPOINT
        if self.TotalRadioButton.isChecked():
            return MutationType.TOTAL
        return MutationType.ONEPOINT