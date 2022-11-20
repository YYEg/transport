def ij(c_min):
    c = np.inf
    for i in range(c_min.shape[0]):
        for j in range(c_min.shape[1]):
            if (c_min[i, j] !=0) and (c_min[i, j]<c):
                c = c_min[i, j]
                i_, j_ = i, j
    return i_, j_


def M_min(a_, b_, c_, print_=False):
    a = np.copy(a_)
    b = np.copy(b_)
    c = np.copy(c_)

    # Проверяем условие замкнутости: если не замкнута - меняем соотвествующие векторы и матрицу трансп. расходов
    if a.sum() > b.sum():
        b = np.hstack((b, [a.sum() - b.sum()]))
        c = np.hstack((c, np.zeros(len(a)).reshape(-1, 1)))
    elif a.sum() < b.sum():
        a = np.hstack((a, [b.sum() - a.sum()]))
        c = np.vstack((c, np.zeros(len(b))))

    m = len(a)
    n = len(b)
    x = np.zeros((m, n), dtype=int)  # создаем матрицу для x и заполняем нулями
    funk = 0
    while True:
        c_min = np.zeros((m, n))
        for i in range(m):
            for j in range(n):
                c_min[i, j] = (c[i, j] * min(a[i], b[j]))  # составляем матрицу суммарных расходов
        i, j = ij(c_min)  # определяем индексы минимального элемента составленной матрицы суммарных расходов
        x_ij = int(min(a[i], b[j]))
        x[i, j] = x_ij  # добавляем элемент x_ij в матрицу x
        funk += int(c_min[i, j])  # добавляем x_ij в итоговую функцию
        a[i] -= x_ij  #
        b[j] -= x_ij  # обновляем векторы a и b
        if print_:
            print('c_min:')
            print(c_min.astype(int))
            print('a: ', a)
            print('b: ', b)
            print()
        if len(c_min[c_min > 0]) == 1:  # повторяем до сходимости метода
            break
    return x, funk  # возращаем матрицу x и целевую функцию