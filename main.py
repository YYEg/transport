import numpy as np


#Проверка открытости/закрытости задачи
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
        print("Задача закрытая", zapSum, "=", potrebSum)
    elif zapSum > potrebSum:
        print("открытая", zapSum, ">", potrebSum)
        valuePotreb = zapSum - potrebSum
        newPotreb = np.hstack((potreb, valuePotreb))
        changed = np.hstack((changed, np.zeros(len(newZapac)).reshape(len(newZapac), 1)))
        print(newPotreb)
        print(changed)
        opPlan(newZapac, newPotreb, changed)
    elif zapSum < potrebSum:
        print("открытая", zapSum, "<", potrebSum)

def opPlan(zapac, potreb, matrix):
    i, j = 0, 0
    m, n = len(zapac), len(potreb)
    oporPlan = np.zeros((m, n), dtype=int)
    functionValue = 0
    while ((i < m) and (j < n)):  # повторяем цикл до сходимости метода
        transported = min(zapac[i], potreb[j])  #берем минимальное значение из Потребностей/Запасов
        functionValue += matrix[i][j] * min(zapac[i], potreb[j])  # записываем в итоговую функцию элемент трат
        zapac[i] -= transported  #
        potreb[j] -= transported  # обновляем векторы a и b
        oporPlan[i][j] = transported  # добавляем элемент transported в матрицу oporPlan

        if zapac[i] > potreb[j]:  # делаем сдвиги при выполнении условий
            j += 1
        elif zapac[i] < potreb[j]:
            i += 1
        else:
            i += 1
            j += 1
    print(oporPlan)
    print(functionValue)
    assessmentMatrix(zapac, potreb, matrix, oporPlan)

def assessmentMatrix(zapac, potreb, matrix, oporPlan):
    Ui, Vj = np.zeros(len(zapac)), np.zeros(len(potreb))

    for i in range(len(zapac)):
        for j in range(len(potreb)):
            if oporPlan[i, j] != 0:  # если элемент матрицы x не равен 0, расчитываем для данных индексов векторы Ui и Vj
                if Vj[j] != 0:
                    Ui[i] = matrix[i, j] - Vj[j]
                else:
                    Vj[j] = matrix[i, j] - Ui[i]

    delta = np.zeros((len(zapac), len(potreb)))
    for i in range(len(zapac)):
        for j in range(len(potreb)):
            delta[i, j] = Ui[i] + Vj[j] - matrix[i, j]  # расчитываем элемент дельта матрицы
    print(delta)


#----------------------------------------------Меню------------------------------------------------------
matrix = np.loadtxt("uslovie.txt", dtype=int) #Загрузка матрицы в программу из файла
zap = np.loadtxt("zapac.txt", dtype=int) #Загрузка запаса в программу из файла
potreb = np.loadtxt("potreb.txt", dtype=int) #Загрузка потребности в программу из файла
(row, col) = matrix.shape #Возвращает размерность массива
isOpen(zap, potreb, matrix)
print(matrix)
print(zap)
print(potreb)

