import numpy as np
from scipy.optimize import linprog


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
        isOpen(newZapac, newPotreb, changed)
    elif zapSum < potrebSum:
        print("открытая", zapSum, "<", potrebSum)

#def opPlan(zapac, potreb, matrix):


#----------------------------------------------Меню------------------------------------------------------
matrix = np.loadtxt("uslovie.txt", dtype=int) #Загрузка матрицы в программу из файла
zap = np.loadtxt("zapac.txt", dtype=int) #Загрузка запаса в программу из файла
potreb = np.loadtxt("potreb.txt", dtype=int) #Загрузка потребности в программу из файла
(row, col) = matrix.shape #Возвращает размерность массива
isOpen(zap, potreb, matrix)
print(matrix)
print(zap)
print(potreb)

