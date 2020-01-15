## @package Graph
# Модуль для хранения графа и его считывания из файла

from datetime import datetime
import numpy as np
import math

## @class Graph
class Graph:

    ## Конструктор
    # @param filepath - путь до файла с описанием графа
    def __init__(self, filepath):
        f = open(filepath, 'r')
        self.__vertexes = int(f.readline().split()[0])
        fpointsline = f.readline().split()
        self.__startpoint, self.__finishpoint = int(fpointsline[0]), int(fpointsline[1])
        self.__starttime = datetime.strptime(f.readline().split()[0], '%H:%M')
        self.__distmatrix = list(np.zeros((self.__vertexes, self.__vertexes)))
        f.readline()
        while True: # считывание длин дорог в графе
            fline = f.readline()
            if fline == '\n':
                break
            else:
                linedata = fline.split()
                i, j, dist = int(linedata[0])-1, int(linedata[1])-1, float(linedata[2])
                self.__distmatrix[i][j] = self.__distmatrix[j][i] = dist
        self.__speedmatrix = [[dict() for j in range(self.__vertexes)] for i in range(self.__vertexes)]
        while True: # считывание ограничений по скорости в определенные промежутки времени на каждой дороге
            fline = f.readline()
            if not fline:
                break
            linedata = fline.split()
            point1, point2, key, start_time, finish_time = int(linedata[0])-1, int(linedata[1])-1, int(linedata[2]), \
                                                           datetime.strptime(linedata[3], '%H:%M'),\
                                                           datetime.strptime(linedata[4], '%H:%M')
            self.__speedmatrix[point1][point2][key] = self.__speedmatrix[point2][point1][key] = [start_time, finish_time]
        f.close()

    ## Функция, возвращающая количество вершин в графе
    # @return количетсво вершин в графе
    def Vertexes(self):
        return self.__vertexes

    ## Функция, возвращающая номер вершины -  начальной точки пути
    # @return номер вершины -  начальной точки пути
    def StartPoint(self):
        return self.__startpoint

    ## Функция, возвращающая номер вершины - конечной точки пути
    # @return yомер вершины - конечной точки пути
    def FinishPoint(self):
        return self.__finishpoint

    ## Функция, возвращающая время начала пути
    # @return dремя начала пути
    def StartTime(self):
        return self.__starttime

    ## Функция, возвращающая матрицу смежности со всеми длинами дорог в графе
    # @return vатрица смежности со всеми длинами дорог в графе
    def DistanceMatrix(self):
        return self.__distmatrix

    ## Функция, возвращающая матрицу смежности с ограничениями по скорости движения в промежутки времени на каждой дороге
    # Матрица смежности имеет структуру словаря
    # @return vатрица смежности со всеми ограничениями по скорости движения в промежутки времени на каждой из дорог
    def SpeedMatrix(self):
        return self.__speedmatrix

    ## Функция, возвращающая число всех возможных различных путей графа
    # @return число всевозможных различных путей графа
    def GetAllDifferentWaysCount(self):
        if self.__vertexes < 2:
            return 0
        elif self.__vertexes == 2:
            return 1
        else:
            sum = 0
            n = self.__vertexes-2
            for k in range(n+1):
                sum += int(math.factorial(n)/math.factorial(n-k))
            return sum
        return 0