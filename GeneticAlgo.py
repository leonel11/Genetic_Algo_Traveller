## @package GeneticAlgo
# Модуль, моделирующий генетический алгоритм

import numpy as np
from datetime import timedelta

from Enums import StartPopulation, NewPopulation, MutationType

## @class GeneticAlgo
class GeneticAlgo:

    ## Конструктор
    # @param graph - граф с описанием городской дорожной сети
    # @param tourchance - вероятность выбора лучшей хромосомы при турнирной селекции (желательно брать значение > 0.5)
    # @param muttype - вид мутации, применяемой к каждой особи новой популяции
    # @param mutchance - вероятность мутации в хромосомы (желательно брать значение < 0.1)
    # @param iters - число итераций генетического алгоритма
    # @param popsize - количество особей в начальной популяции особей, с которой начнет работу генетический алгоритм
    # @param startpoptype - способ формирования начальной популяции для генетического алгоритма
    # @param newpoptype - способ формирования новой популяции для генетического алгоритма
    def __init__(self, graph, tourchance, muttype, mutchance, iters, popsize, startpoptype, newpoptype):
        self.__graph = graph
        self.__tournamentchance = tourchance
        self.SetMutationType(muttype)
        self.__mutationchance = mutchance
        self.__iterations = iters
        self.__populationsize = popsize
        self.__startpopulationtype = startpoptype
        self.__newpopulationtype = newpoptype
        self.__population = []
        self.__bestway = []

    ## Установка значения - вида мутации генетического алгоритма
    # @param muttype - вид мутации, применяемой к каждой особи новой популяции
    def SetMutationType(self, muttype):
        if self.__graph.Vertexes() == 3:
            self.__mutationtype = MutationType.ONEPOINT
        self.__mutationtype = muttype

    ## Формирование изначальной, первой популяции, для особей которой начнет работу генетический алгоритм
    def GenerateFirstStartPopulation(self):
        popsize = self.__populationsize
        while len(self.__population) < popsize: # пока не будет сформирована популяция нужного размера
            self.__population.append(self.GetGeneratedValidRandomHromosome())
            self.DeleteDublicatePopulationHromosomes()
        for idx in range(len(self.__population)): # дополнение нулями до нужного размера каждой хромосомы популяции
            self.AppendHromosomeZeros(self.__population[idx], self.__graph.Vertexes())

    ## Генерация валидной случайной хроосомы
    # Валидная хромосома - хромосома, начинающаяся со стартовой точки пути и заканчивающаяся финишной точки пути
    # @return сгенерированная случайным образом валидная хромосома
    def GetGeneratedValidRandomHromosome(self):
        # формирование списка вершин, которые годятся для формирования хромосомы (все, кроме начальной и конечной точки пути)
        listvertixes = list(range(1, self.__graph.Vertexes() + 1))
        listvertixes.remove(self.__graph.StartPoint())
        listvertixes.remove(self.__graph.FinishPoint())
        # формирование валидной хромосомы
        hromosome = [self.__graph.StartPoint()] # добавление номера вершины - начальной точки пути
        gens = np.random.randint(0, len(listvertixes) + 1) # количество генов, которые будут включены в валидную
                                                           # хромосому помимо начальной и конечной точки пути
        for i in range(gens):
            if len(listvertixes) != 0:
                vertex = listvertixes[np.random.randint(0, len(listvertixes))] # выбор вершины, добавляемой в хромосому
                hromosome.append(vertex) # добавление выбранной вершины в хромосому
                listvertixes.remove(vertex) # удаление только что добавленного в хромосому гена из списка вершин,
                                            # которые годщятся для формирования хромосомы
        hromosome.append(self.__graph.FinishPoint()) # добавление номера вершины - конечной точки пути
        return hromosome

    ## Удаление повторяющихся хромосом из текущей популяции
    def DeleteDublicatePopulationHromosomes(self):
        i = 0
        while i < len(self.__population)-1:
            j = i+1
            while (j < len(self.__population)):
                if self.__population[i] == self.__population[j]:
                    self.__population.pop(j)
                else:
                    j += 1
            i += 1
        self.__populationsize = len(self.__population) # фиксирование изменения размера текущей популяции

    ## Дополнение нулями хромосомы до нужного размера
    # @param hromosome - хромосома, которая подвергнется изменениям
    # @param size - необходимый размер хромосомы
    def AppendHromosomeZeros(self, hromosome, size):
        while len(hromosome) < size: # пока хромосома не станет нужной длины
            hromosome.append(0)

    ## Удаление из хромосомы всех нулей
    # @param hromosome - хромосома, которая подвергнется изменениям
    # @return хромосома без нулей
    def RemoveHromosomeZeros(self, hromosome):
        return list(filter(lambda gen: gen != 0, hromosome))

    ## Булева функция, которая проверяет, содержит ли хромосома цикл (повторяющиеся значения генов)
    # @param hromosome - хромосома, для которой требуется провести проверку
    # @return True or False
    def IsHromosomeContainCycle(self, hromosome):
        i = 0
        while (i < len(hromosome)-1) and (hromosome[i] != 0):
            j = i+1
            while (j < len(hromosome)) and (hromosome[j] != 0):
                if hromosome[i] == hromosome[j]:
                    return True
                else:
                    j += 1
            i += 1
        return False

    ## Булева функция, которая проверяет является ли хромосома нужным для решения задачи путем
    # Хромосома является нужным путем для решения задачи, если она начинается с номера вершины - стартовой точки пути и
    # заканчивается номером вершины - финишной точкой пути (не считая нулей)
    # @param hromosome - хромосома, для которой требуется провести проверку
    # @return True or False
    def IsNeededWay(self, hromosome):
        # проверка, начинается ли хромосома с номера вершины - стартовой точкой пути
        if hromosome[0] != self.__graph.StartPoint():
            return False
        # проверка, содержит ли хромосома номер вершины - конечную точку пути
        if self.__graph.FinishPoint() not in hromosome:
            return False
        # проверка, оканчивается ли хромосома номером вершины - конечной точкой пути (не считая нулей)
        for i in range(1, len(hromosome)):
            if hromosome[-i] != 0:
                if hromosome[-i] == self.__graph.FinishPoint():
                    return True
                else:
                    return False
        return False

    ## Булева функция, которая проверяет вляется ли хромосома валидной для решения задачи
    # Валидная для решения задачи хромосомы начинается с номера вершины - стартовой точкой пути и
    # заканчивается номером вершины - финишной точкой пути.
    # Также хромосома не должна содержать циклов (повторяющихся значений генов)
    # @return True or False
    def IsValidHromosome(self, hromosome):
        if not hromosome:
            return False
        if not self.IsNeededWay(hromosome):
            return False
        if self.IsHromosomeContainCycle(hromosome):
            return False
        return True

    # Подсчет длины пути
    # @param hromosome - хромосома-путь, по которой происходит движение
    # @return длина пути
    def GetHromosomeWayLength(self, hromosome):
        if not hromosome:
            return -1.0
        if not self.IsValidHromosome(hromosome):
            return -1.0
        result = 0.0
        i = 0
        # подсчет суммарной длины пути при последовательном передвижении от одной точки пути до другой
        while (i < len(hromosome)-1) and (hromosome[i] != self.__graph.FinishPoint()):
            dist = self.__graph.DistanceMatrix()[hromosome[i]-1][hromosome[i+1]-1]
            if dist <= 0:
                return -1.0
            else:
                result += dist
            i += 1
        return result

    # Подсчет затраченного в пути времени
    # @param hromosome - хромосома-путь, по которой происходит движение
    # @return время в пути
    def GetHromosomeWayTime(self, hromosome):
        if not hromosome:
            return -1.0
        if not self.IsValidHromosome(hromosome):
            return -1.0
        current_time = self.__graph.StartTime() # переменная, контролирующая текущий момент времени,
                                                # в котором сейчас находится движущийся объект
        result = 0.0
        i = 0
        # подсчет суммарного времени, потраченного при последовательном передвижении от одной точки пути до другой
        while (i < len(hromosome)-1) and (hromosome[i] != self.__graph.FinishPoint()):
            dist = self.__graph.DistanceMatrix()[hromosome[i]-1][hromosome[i+1]-1]
            speeds = self.__graph.SpeedMatrix()[hromosome[i]-1][hromosome[i+1]-1]
            listspeeds = list(speeds.keys()) # список возможных скоростей движения по данной дороге
            if not listspeeds:
                return -1.0
            else:
                listkeys = listspeeds
                flag = False # булева переменная, контролирующая процесс выбора нужной скорости движения по данной дороге
                for j in range(len(listkeys)-1): # перебор всех возможных значений скоростей на данной дороге
                    if not flag:
                        speed = float(listkeys[j])
                        if speed <= 0.0:
                            return -1.0
                        if (current_time >= speeds[listkeys[j]][0]) and (current_time <= speeds[listkeys[j]][1]):
                            value = int(3600*dist/speed)
                            result += value
                            current_time = current_time + timedelta(seconds=value)
                            flag = True
                if not flag:
                    speed = float(list(speeds.keys())[-1])
                    value = int(3600*dist/speed)
                    result += value
                    current_time = current_time + timedelta(seconds=value)
            i += 1
        return result

    ## Выбор наиболее приспособленной хромосомы из 2
    # При выборе наиболее приспособленной хромосомы в первую очередь учитывается время пути, а потом его длина
    # @param hromosome1 - первая хромосома
    # @param hromosome2 - вторая хромосома
    # @return наиболее приспособленная хромосома из 2
    def GetBetterHromosome(self, hromosome1, hromosome2):
        if self.GetHromosomeWayTime(hromosome1) <= 0.0:
            if self.GetHromosomeWayTime(hromosome2) <= 0.0:
                return []
            else:
                return hromosome2
        elif self.GetHromosomeWayTime(hromosome2) <= 0.0:
            if self.GetHromosomeWayTime(hromosome1) <= 0.0:
                return []
            else:
                return hromosome1
        elif self.GetHromosomeWayTime(hromosome1) < self.GetHromosomeWayTime(hromosome2):
            return hromosome1
        elif self.GetHromosomeWayTime(hromosome1) > self.GetHromosomeWayTime(hromosome2):
            return hromosome2
        elif self.GetHromosomeWayLength(hromosome1) >= self.GetHromosomeWayLength(hromosome2):
            return hromosome2
        else:
            return hromosome1
        return []

    ## Выбор наиболее приспособленной хромосомы из всех среди текущей популяции
    # @return наилучшая хромосома текущей популяции
    def GetBestPopulationHromosome(self):
        if not self.__population:
            return []
        best_hromosome = self.__population[-1] # в начале наилучшей особью считается последняя хросома в списке популяции
        for i in range(len(self.__population)-1): # перебор хромосом популяции
            best_hromosome = self.GetBetterHromosome(self.__population[i], best_hromosome)
        return best_hromosome

    ## Выбор наименее приспособленной хромосомы из всех среди данной популяции
    # @param population - популяция для выбора наихудшей хроморсомы
    # @return наихудшая хромосома данной популяции
    def GetWorstPopulationHromosome(self, population):
        if not population:
            return []
        worst_hromosome = population[-1] # в начале наихудшей особью считается последняя хросома в данном списке популяции
        for i in range(len(population)-1): # перебор хромосом популяции
            # составление списка хромосом для выбора наихудшей.
            # Список состоит из 2 хромосом - наихудшей на данной момент особи и  текущей рассматриваемой особи из популяции
            two_hromosomes = [population[i], worst_hromosome]
            # далее выбирается наиболее приспособленная хромосома из 2. А значит оставшаяся - наименее приспособленная
            best_hromosome = self.GetBetterHromosome(two_hromosomes[0], two_hromosomes[1])
            if best_hromosome:
                two_hromosomes.remove(best_hromosome)
                worst_hromosome = two_hromosomes[0]
        return worst_hromosome

    ## Сдвиг нулей в хромосоме в конец
    # @param hromosome - хромосома, которая подвергнется изменениям
    # @return хромосома со сдвинутыми вправо нулями
    def ZeroShiftInHromosome(self, hromosome):
        result = [0 for i in range(self.__graph.Vertexes())]
        idx = 0
        for gen in hromosome:
            if gen != 0:
                result[idx] = gen
                idx += 1
        return result

    ## Генерация новой начальной популяции для генетического алгоритма
    # @return новая сгенерированная популяция
    def GetGeneratedStartNewPopulation(self):
        newpopulation = []
        # формирование начальной популяции для генетического алгоритма в зависимости от способа
        if self.__startpopulationtype == StartPopulation.ELITE:
            newpopulation = [self.GetBestPopulationHromosome()]
        if self.__startpopulationtype == StartPopulation.FULL:
            newpopulation = self.__population
        return newpopulation

    ## Чистка текущей популяции
    def CleanPopulation(self):
        self.DeleteDublicatePopulationHromosomes()
        i = 0
        while i < len(self.__population):
            if not self.IsValidHromosome(self.__population[i]):
                self.__population.remove(self.__population[i])
            else:
                i += 1
        if self.__newpopulationtype == NewPopulation.GENITOR:
            while (len(self.__population) > self.__populationsize):
                self.__population.remove(self.GetWorstPopulationHromosome(self.__population))
        self.__populationsize = len(self.__population)

    ## Добавление хромосомы в данную популяцию
    # @param hromosome - хромосома для добавления
    # @param population - популяция, в которую будет добавлена хромосома
    def AddHromosomeToPopulation(self, hromosome, population):
        # добавление хромосомы в данную популяцию в зависимости от способа формирования новой популяции
        if self.__newpopulationtype == NewPopulation.CLASSIC:
            population.append(hromosome)
        if self.__newpopulationtype == NewPopulation.GENITOR:
            if (self.IsValidHromosome(hromosome)):
                worst_hromosome =  self.GetWorstPopulationHromosome(population)
                population[population.index(worst_hromosome)] = hromosome

    ## Метод турнирной селекции для текущей популяции
    # @return хромосома, выбранная в результате турнирной селекции
    def TournamentSelectionFromPopulation(self):
        hromosome = []
        if (self.__population):
            hromosome1 = self.__population[np.random.randint(0, len(self.__population))]
            hromosome2 = self.__population[np.random.randint(0, len(self.__population))]
            p = np.random.random() # значение вероятности, которое будет сравниваться с вероятностью выбора
                                   # лучшей хромосомы в турнирной селекции
            if p <= self.__tournamentchance:
                hromosome = self.GetBetterHromosome(hromosome1, hromosome2)
            else:
                # выбор случайной хромосомы в случае, если наилучшая не была выбрана
                hromosome = np.random.choice([hromosome1, hromosome2])
            if not hromosome:
                hromosome = hromosome1
                if not hromosome1:
                    hromosome = hromosome2
        return hromosome

    ## Скрещивание 2 хромосом
    # @param hromosome1 - первая хромосома
    # @param hromosome2 - вторая хромосома
    # @return 2 скрещенные хромосомы
    def Junction(self, hromosome1, hromosome2):
        if not hromosome1 or not hromosome2 or (self.__graph.Vertexes() <= 2):
            return hromosome1, hromosome2
        # выбор 2 точек скрещивания
        numb1 = numb2 = np.random.randint(1, self.__graph.Vertexes())
        while (numb2 == numb1):
            numb2 = np.random.randint(1, self.__graph.Vertexes())
        # упорядочивание по возрастанию позиций скрещивания
        pos1, pos2 = min(numb1, numb2), max(numb1, numb2)
        # применение оператора скрещивания
        son_hromosome1 = [0 for idx in range(self.__graph.Vertexes())]
        son_hromosome2 = [0 for idx in range(self.__graph.Vertexes())]
        son_hromosome1[:pos1] = hromosome1[:pos1]
        son_hromosome2[:pos1] = hromosome2[:pos1]
        son_hromosome1[pos1:pos2] = hromosome2[pos1:pos2]
        son_hromosome2[pos1:pos2] = hromosome1[pos1:pos2]
        son_hromosome1[pos2:] = hromosome1[pos2:]
        son_hromosome2[pos2:] = hromosome2[pos2:]
        son_hromosome1 = self.ZeroShiftInHromosome(son_hromosome1)
        son_hromosome2 = self.ZeroShiftInHromosome(son_hromosome2)
        return son_hromosome1, son_hromosome2

    ## Мутация данной хромосомы
    # @param hromosome - хромосома, которая будет мутировать
    # @return мутировавшая хромосома
    def Mutation(self, hromosome):
        if not hromosome or (self.__graph.Vertexes() <= 2):
            return hromosome
        # формирование списка точек мутации в зависимости от вида мутации
        listnumbers = []
        if self.__mutationtype == MutationType.ONEPOINT:
            listsize = 1
        elif self.__mutationtype == MutationType.MULTIPOINT:
            listsize = np.random.randint(2, self.__graph.Vertexes()-1)
        else:
            listnumbers = list(range(1, self.__graph.Vertexes()-1))
        if self.__mutationtype != MutationType.TOTAL:
            i = 0
            while i<listsize:
                numb = np.random.randint(0, self.__graph.Vertexes())
                if numb not in listnumbers:
                    listnumbers.append(numb)
                    i += 1
        # применение оператора мутации
        for i in range(len(listnumbers)):
            p = np.random.random()
            if p <= self.__mutationchance:
                hromosome[listnumbers[i]] = np.random.randint(1, self.__graph.Vertexes()+1)
            hromosome = self.ZeroShiftInHromosome(hromosome)
        return hromosome

    ## Эволюция текущей популяции (генетический алгоритм)
    def Evolution(self):
        newpopulation = self.GetGeneratedStartNewPopulation()
        iter = 0 # номер текущей проделанной итерации
        validchange_count = 0 # количество формирований новых валидных хромосом.
                              # Переменная позволяет улучшить качество новой формируемой популяции
        runningalgo = True # переменая, необходимая для контроля процесса формирования новой популяции
        # пока не проделано нужное число итераций генетического алгоритма или популяция не стала состоять из одной особи
        while (iter < self.__iterations) and (len(self.__population) > 1) and runningalgo:
            while validchange_count < self.__populationsize:
                hromosome1, hromosome2 = self.TournamentSelectionFromPopulation(), \
                                         self.TournamentSelectionFromPopulation()
                hromosome1, hromosome2 = self.Junction(hromosome1, hromosome2)
                hromosome1, hromosome2 = self.Mutation(hromosome1), self.Mutation(hromosome2)
                if self.IsValidHromosome(hromosome1) or self.IsValidHromosome(hromosome2):
                    # увеличение значения в случае, если при формировании новых хромосом хоть одна из них валидна
                    validchange_count += 1
                if self.IsValidHromosome(hromosome1):
                    self.AddHromosomeToPopulation(hromosome1, newpopulation)
                if self.IsValidHromosome(hromosome2):
                    self.AddHromosomeToPopulation(hromosome2, newpopulation)
            prevpopulation = self.__population
            self.__population = newpopulation
            self.CleanPopulation()
            if self.__population == prevpopulation:
                # остановка алгоритма в случае если новая сформированная популяция не отличается от текущей популяции
                runningalgo = False
            newpopulation = self.GetGeneratedStartNewPopulation()
            iter += 1

    ## Поиск кратчайшего пути с учетом времени и длины пути
    # @return кратчайший путь
    def FindQuickestWay(self):
        self.GenerateFirstStartPopulation()
        self.Evolution()
        self.__bestway = self.RemoveHromosomeZeros(self.GetBestPopulationHromosome())
        return self.__bestway