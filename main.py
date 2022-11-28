import numpy as np

def minIndex(opElement, zapac, potreb): #функция нахождения минимального элемента в матрице, для постройки опорного плана
    c = 10000000000000000000
    minI = 0
    minJ = 0
    maxZapac = 0
    maxPotreb = 0
    for i in range(len(zapac)):
        if maxZapac < zapac[i]:
            maxZapac = zapac[i]
            minI = i
    for i in range(len(potreb)):
        if maxPotreb < potreb[i]:
            maxPotreb = potreb[i]
            minJ = i
    for i in range(opElement.shape[0]):
        for j in range(opElement.shape[1]):
            if (opElement[i, j] != 0) and (opElement[i, j] < c):
                c = opElement[i, j]
                minI = i
                minJ = j
    return minI, minJ



def isOpen(zapac, potreb, matrix):
    zapSum = 0
    potrebSum = 0
    changed = np.copy(matrix)
    newPotreb = np.copy(potreb)
    newZapac = np.copy(zapac)
    for i in range(len(zap)):
        zapSum += zap[i]
    for i in range(len(newPotreb)):
        potrebSum += newPotreb[i]
    if zapSum == potrebSum:
        print("----------------------------------------------------------------------------------------")
        print("Задача закрытая", zapSum, "=", potrebSum)
        print("----------------------------------------------------------------------------------------")
    elif zapSum > potrebSum:
        print("----------------------------------------------------------------------------------------")
        print("Задача открытая, нужен эффективный потребитель ", zapSum, ">", potrebSum)
        valuePotreb = zapSum - potrebSum
        newPotreb = np.hstack((potreb, valuePotreb))
        changed = np.hstack((changed, np.zeros(len(newZapac)).reshape(len(newZapac), 1)))
        print("Измененная строка с запасами:")
        print(newZapac)
        print("Измененная матрица:")
        print(changed)
        print("----------------------------------------------------------------------------------------")
    elif zapSum < potrebSum:
        print("----------------------------------------------------------------------------------------")
        print("Задача открытая, нужен эффективный поставщик ", zapSum, "<", potrebSum)
        valueZapac = potrebSum - zapSum
        newZapac = np.hstack((zapac, valueZapac))
        changed = np.vstack((changed, np.zeros(len(potreb))))
        print("Измененная строка с запасами:")
        print(newZapac)
        print("Измененная матрица:")
        print(changed)
        print("----------------------------------------------------------------------------------------")
    return newZapac, newPotreb, changed


def minOpPlan(zapac, potreb, matrix):
    m = len(zapac)
    n = len(potreb)
    funk = 0
    opPlan = np.zeros((m, n), dtype=int)
    minArray = np.copy(matrix)
    count = 0
    while True:
        count += 1
        zapSum = 0
        i, j = minIndex(minArray, zapac, potreb)
        x_ij = int(min(zapac[i], potreb[j]))
        opPlan[i, j] = x_ij
        zapac[i] -= x_ij
        potreb[j] -= x_ij
        funk += int(minArray[i, j] * opPlan[i, j])
        minArray[i, j] = 0
        for i in range(len(zapac)):
            zapSum += zapac[i]
        if zapSum == 0:
            break
    return opPlan, funk

def assessmentMatrix(zapac, potreb, matrix, opPlan, check):
    delta = np.zeros((len(zapac), len(potreb)))
    m, n = len(zapac), len(potreb)
    Ui, Vj = np.zeros(len(zapac)), np.zeros(len(potreb)) #массивы для Ui и Vj
    UboolI, VboolJ = np.zeros(len(zapac)), np.zeros(len(potreb)) #массивы для определения наличия значения в массивах Ui и Vj
    for i in range(m): UboolI[i] = False
    for j in range(n): VboolJ[j] = False
    Ui[0] = 0
    UboolI[0] = True
    counter = 0


    while counter <= (n+m):
        for i in range (m):
            if UboolI[i] == True:
                for j in range (n):
                    if opPlan[i][j] != 0:
                        if VboolJ[j] == False:
                            Vj[j] = matrix[i][j] - Ui[i]
                            VboolJ[j] = True
        for j in range (n):
            if VboolJ[j] == True:
                for i in range (m):
                    if opPlan[i][j] != 0:
                        if UboolI[i] == False:
                            Ui[i] = matrix[i][j] - Vj[j]
                            UboolI[i] = True
        counter += 1

    for i in range(len(zapac)): # расчитываем оценочную матрицу
        for j in range(len(potreb)):
            if(opPlan[i][j] == 0):
                opPlan[i, j] = -1
    for i in range(len(zapac)): # расчитываем оценочную матрицу
        for j in range(len(potreb)):
            if(opPlan[i][j] == -1):
                delta[i, j] = matrix[i, j] - (Ui[i] + Vj[j])

    print("Оценочная матрица:")
    print(delta)
    print("Ui:")
    print(Ui)
    print("Vj:")
    print(Vj)
    for i in range(len(zapac)):
        for j in range(len(potreb)):
            if delta[i, j] < 0:
                check = False

    if check == True:
        print("----------------------------------------------------------------------------------------")
        print("!План оптимальный!")
        print("----------------------------------------------------------------------------------------")
    else:
        print("----------------------------------------------------------------------------------------")
        print("!План НЕ оптимальный!")
        print("----------------------------------------------------------------------------------------")
    return m, n, opPlan, delta, check

def cycle(m, n, opPlan, delta, zapac, potreb):
    deltaMinEl = 0
    k, l = 0, 0
    for i in range(m):
        for j in range(n):
            if opPlan[i][j] == -1:
                if delta[i][j] < deltaMinEl:
                    deltaMinEl = delta[i][j]
                    k, l = i, j
    cycleMatrix = np.zeros((len(zapac), len(potreb))) #матрица, указывающая на элементы цикла
    for i in range(m):
        for j in range(n):
           cycleMatrix[i][j] = -1
    findMin = findCycleHorizontal(k, l, k, l, m, n, opPlan, cycleMatrix, 0, -1)
    for i in range(m):
        for j in range(n):
            if cycleMatrix[i][j] != -1:
                opPlan[i][j] = opPlan[i][j] + cycleMatrix[i][j]
                if (i == k) and (j == l):
                    opPlan[i][j] += 1
                if (cycleMatrix[i][j] <= 0) and (opPlan[i][j] == 0):
                    opPlan[i][j] = -1
    opPlan[k][l] = cycleMatrix[k][l]
    return opPlan




def findCycleHorizontal(nextI, nextJ, II, JJ, n, m, opPlan, cycleMatrix, numEl, minmin):
    OutRezult = -1
    for j in range(m):
        if (opPlan[nextI][j] >= 0 and j != nextJ) or (j == JJ and nextI == II and numEl != 0):
            numEl += 1
            minminLast = -1
            if (numEl % 2) == 1:
                minminLast = minmin
                if minmin < 0:
                    minmin = opPlan[nextI][j]
                elif minmin > opPlan[nextI][j] >= 0:
                    minmin = opPlan[nextI][j]
            if (j == JJ) and (nextI == II) and (numEl % 2) == 0:
                cycleMatrix[II][JJ] = minmin
                return minmin
            else:
               OutRezult = findCycleVertical(nextI, j, II, JJ, n, m, opPlan, cycleMatrix, numEl, minmin)
            if OutRezult >= 0:
                if numEl % 2 == 0:
                    cycleMatrix[nextI][j] = cycleMatrix[II][JJ]
                else:
                    cycleMatrix[nextI][j] = -cycleMatrix[II][JJ]
                break
            else:
                numEl -= 1
                if minminLast >= 0:
                    minmin = minminLast
    return OutRezult


def findCycleVertical(nextI, nextJ, II, JJ, n, m, opPlan, cycleMatrix, numEl, minmin):
    outRezult = -1
    i = 0
    for i in range(n):
        if (opPlan[i][nextJ] >= 0 and i != nextI) or (nextJ == JJ and i == II and numEl != 0):
            numEl += 1
            minminLast = -1
            if (numEl % 2) == 1:
                minminLast = minmin
                if minmin < 0:
                    minmin = opPlan[i][nextJ]
                elif minmin > opPlan[i][nextJ] >= 0:
                    minmin = opPlan[i][nextJ]
            if (i == II) and (nextJ == JJ) and (numEl % 2) == 0:
                cycleMatrix[II][JJ] = minmin
                return minmin
            else:
                outRezult = findCycleHorizontal(i, nextJ, II, JJ, n, m, opPlan, cycleMatrix, numEl, minmin)
            if outRezult >= 0:
                if numEl % 2 == 0:
                    cycleMatrix[i][nextJ] = cycleMatrix[II][JJ]
                else:
                    cycleMatrix[i][nextJ] = -cycleMatrix[II][JJ]
                break
            else:
                numEl -= 1
                if minminLast >= 0:
                    minmin = minminLast
    return outRezult

#----------------------------------------------Меню------------------------------------------------------
while(True): #Вывод информации на экран
    print("----------------------------------------------------------------------------------------")
    print("---Лабораторная работа по ИО №3---")
    print("\n1 - решение открытой транспортной задачи с эффективным потребителем\n")
    print("2 - решение открытой транспортной задачи с эффективным поставщиком\n")
    print("3 - решение закрытой транспортной задачи\n")
    print("4 - выход\n")
    print("----------------------------------------------------------------------------------------")
    choice = int(input())
    if choice == 1:
        matrix = np.loadtxt("testusl.txt", dtype=int)  # Загрузка матрицы в программу из файла
        zap = np.loadtxt("testzapac.txt", dtype=int)  # Загрузка запаса в программу из файла
        potreb = np.loadtxt("testpotr.txt", dtype=int)  # Загрузка потребности в программу из файла
        print("----------------------------------------------------------------------------------------")
        print("Заданное условие:")
        print("Матрица перевозок")
        print(matrix)
        print("Запасы")
        print(zap)
        print("Потребности")
        print(potreb)
        print("----------------------------------------------------------------------------------------")
        print("Решение задачи:")
        newZapac, newPotreb, changed = isOpen(zap, potreb,
                                              matrix)  # функция возвращает измененную матрицу и запас/потребность
        newNewZapac, newNewPotreb = np.copy(newZapac), np.copy(newPotreb)  # копирование матриц для работы с ними
        opPlan, fuctionValue = minOpPlan(newNewZapac, newNewPotreb,
                                         changed)  # функция возвращает опорный план, значение функции
        print('Опорный план по методу минимального элемента: \n', opPlan)
        check = True
        m, n, opPlan, delta, check = assessmentMatrix(newZapac, newPotreb, changed, opPlan,
                                                      check)  # вывод оценочной матрицы
        while check == False:
            opPlan = cycle(m, n, opPlan, delta, newZapac, newPotreb)
            for i in range(m):
                for j in range(n):
                    if opPlan[i][j] == -1:
                        opPlan[i][j] = 0
            check = True
            m, n, opPlan, delta, check = assessmentMatrix(newZapac, newPotreb, changed, opPlan, check)
        print("Значение целевой функции:")
        funk = 0
        for i in range(m):
            for j in range(n):
                if opPlan[i][j] == -1:
                    opPlan[i][j] = 0
        for i in range(m):
            for j in range(n):
                funk += int(changed[i, j] * opPlan[i, j])
        fuctionValue = funk
        print(fuctionValue)
        print("----------------------------------------------------------------------------------------")
    if choice == 2:
        matrix = np.loadtxt("uslovie.txt", dtype=int)  # Загрузка матрицы в программу из файла
        zap = np.loadtxt("zapac.txt", dtype=int)  # Загрузка запаса в программу из файла
        potreb = np.loadtxt("potreb.txt", dtype=int)  # Загрузка потребности в программу из файла
        print("----------------------------------------------------------------------------------------")
        print("Заданное условие:")
        print("Матрица перевозок")
        print(matrix)
        print("Запасы")
        print(zap)
        print("Потребности")
        print(potreb)
        print("----------------------------------------------------------------------------------------")
        print("Решение задачи:")
        newZapac, newPotreb, changed = isOpen(zap, potreb, matrix)  # функция возвращает измененную матрицу и запас/потребность
        newNewZapac, newNewPotreb = np.copy(newZapac), np.copy(newPotreb)  # копирование матриц для работы с ними
        opPlan, fuctionValue = minOpPlan(newNewZapac, newNewPotreb, changed)  # функция возвращает опорный план, значение функции
        print('Опорный план по методу минимального элемента: \n', opPlan)
        check = True
        m, n, opPlan, delta, check = assessmentMatrix(newZapac, newPotreb, changed, opPlan, check)  # вывод оценочной матрицы
        count = 2
        while check == False:
            opPlan = cycle(m, n, opPlan, delta, newZapac, newPotreb)
            for i in range(m):
                for j in range(n):
                    if opPlan[i][j] == -1:
                        opPlan[i][j] = 0
            print('Опорный план после цикла, иттерация ', count, '\n', opPlan)
            check = True
            m, n, opPlan, delta, check = assessmentMatrix(newZapac, newPotreb, changed, opPlan, check)
            count += 1
        print("Значение целевой функции:")
        funk = 0
        for i in range(m):
            for j in range(n):
                if opPlan[i][j] == -1:
                    opPlan[i][j] = 0
        for i in range(m):
            for j in range(n):
                funk += int(changed[i, j] * opPlan[i, j])
        fuctionValue = funk
        print(fuctionValue)
        print("----------------------------------------------------------------------------------------")
    if choice == 3:
        matrix = np.loadtxt("uslovie.txt", dtype=int)  # Загрузка матрицы в программу из файла
        zap = np.loadtxt("zapacThird.txt", dtype=int)  # Загрузка запаса в программу из файла
        potreb = np.loadtxt("potreb.txt", dtype=int)  # Загрузка потребности в программу из файла
        print("----------------------------------------------------------------------------------------")
        print("Заданное условие:")
        print("Матрица перевозок")
        print(matrix)
        print("Запасы")
        print(zap)
        print("Потребности")
        print(potreb)
        print("----------------------------------------------------------------------------------------")
        print("Решение задачи:")
        newZapac, newPotreb, changed = isOpen(zap, potreb,
                                              matrix)  # функция возвращает измененную матрицу и запас/потребность
        newNewZapac, newNewPotreb = np.copy(newZapac), np.copy(newPotreb)  # копирование матриц для работы с ними
        opPlan, fuctionValue = minOpPlan(newNewZapac, newNewPotreb,
                                         changed)  # функция возвращает опорный план, значение функции
        print('Опорный план по методу минимального элемента: \n', opPlan)
        check = True
        m, n, opPlan, delta, check = assessmentMatrix(newZapac, newPotreb, changed, opPlan,
                                                      check)  # вывод оценочной матрицы
        while check == False:
            opPlan = cycle(m, n, opPlan, delta, newZapac, newPotreb)
            for i in range(m):
                for j in range(n):
                    if opPlan[i][j] == -1:
                        opPlan[i][j] = 0
            check = True
            m, n, opPlan, delta, check = assessmentMatrix(newZapac, newPotreb, changed, opPlan, check)
        print("Значение целевой функции:")
        funk = 0
        for i in range(m):
            for j in range(n):
                if opPlan[i][j] == -1:
                    opPlan[i][j] = 0
        for i in range(m):
            for j in range(n):
                print(changed[i, j])
                funk += int(changed[i, j] * opPlan[i, j])
        fuctionValue = funk
        print(fuctionValue)
        print("----------------------------------------------------------------------------------------")
    if choice == 4:
        break

