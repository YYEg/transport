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
        print("----------------------------------------------------------------------------------------")
        print(count, " итерация опорного плана")
        print('Оптимальный план:')
        print(opPlan.astype(int))
        print('Запас: ', zapac)
        print('Потребность: ', potreb)
        print("----------------------------------------------------------------------------------------")
        for i in range(len(zapac)):
            zapSum += zapac[i]
        if zapSum == 0:
            break
    return opPlan, funk

def assessmentMatrix(zapac, potreb, matrix, opPlan):
    delta = np.zeros((len(zapac), len(potreb)))
    Ui, Vj = np.zeros(len(zapac)), np.zeros(len(potreb)) #расчитываем для данных индексов векторы Ui и Vj
    Ui[0] = 0
    for i in range(len(zapac)):
        for j in range(len(potreb)):
            if opPlan[i, j] != 0:
                if Vj[j] != 0:
                    Ui[i] = matrix[i, j] - Vj[j]
                else:
                    Vj[j] = matrix[i, j] - Ui[i]
    for i in range(len(zapac)): # расчитываем оценочную матрицу
        for j in range(len(potreb)):
            delta[i, j] = Ui[i] + Vj[j] - matrix[i, j]
    print("Оценочная матрица:")
    print(delta)
    print("Ui:")
    print(Ui)
    print("Vj:")
    print(Vj)
    check = True
    for i in range(len(zapac)):
        for j in range(len(potreb)):
            if delta[i, j] > 0:
                check = False
    if check == True:
        print("----------------------------------------------------------------------------------------")
        print("!План оптимальный!")
        print("----------------------------------------------------------------------------------------")
    else:
        print("----------------------------------------------------------------------------------------")
        print("!План НЕ оптимальный!")
        print("----------------------------------------------------------------------------------------")
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
        matrix = np.loadtxt("uslovie.txt", dtype=int)  # Загрузка матрицы в программу из файла
        zap = np.loadtxt("zapaсSecond.txt", dtype=int)  # Загрузка запаса в программу из файла
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
        assessmentMatrix(newZapac, newPotreb, changed, opPlan)  # вывод оценочной матрицы
        print("Значение целевой функции:")
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
        newZapac, newPotreb, changed = isOpen(zap, potreb,
                                              matrix)  # функция возвращает измененную матрицу и запас/потребность
        newNewZapac, newNewPotreb = np.copy(newZapac), np.copy(newPotreb)  # копирование матриц для работы с ними
        opPlan, fuctionValue = minOpPlan(newNewZapac, newNewPotreb,
                                         changed)  # функция возвращает опорный план, значение функции
        print('Опорный план по методу минимального элемента: \n', opPlan)
        assessmentMatrix(newZapac, newPotreb, changed, opPlan)  # вывод оценочной матрицы
        print("Значение целевой функции:")
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
        assessmentMatrix(newZapac, newPotreb, changed, opPlan)  # вывод оценочной матрицы
        print("Значение целевой функции:")
        print(fuctionValue)
        print("----------------------------------------------------------------------------------------")
    if choice == 4:
        break

