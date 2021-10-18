class IET:
    def __init__(self):
        self.permutation = [0, 1]
        self.inverse_permutation = [0, 1]
        self.lengths_before = [0, 1]
        self.lengths_after = [0, 1]

    def set_via_permutation(self, permutation, lengths_before):
        # set IET via _permutation_ and _lengths_before_
        # supposed that len(_permutation_) == len(_lengths_before_)
        # perhaps improve later
        # always supposed that _permutation_ IS A PERMUTATION
        self.permutation = permutation
        self.lengths_before = lengths_before

        self.inverse_permutation = [0] * len(self.permutation)
        self.lengths_after = [0] * len(self.permutation)

        for i in range(len(self.permutation)):
            self.inverse_permutation[self.permutation[i]] = i
            self.lengths_after[self.permutation[i]] = self.lengths_before[i]

    def set_via_inverse_permutation(self, inverse_permutation, lengths_after):
        self.inverse_permutation = inverse_permutation
        self.lengths_after = lengths_after

        self.permutation = [0] * len(self.inverse_permutation)
        self.lengths_before = [0] * len(self.lengths_after)

        for i in range(len(self.inverse_permutation)):
            self.permutation[self.inverse_permutation[i]] = i
            self.lengths_before[self.inverse_permutation[i]] = self.lengths_after[i]

    def right_step_when_origin_is_smaller(self):
        for i in range(3):
            self.lengths_before[self.inverse_permutation[-1]][i] -= self.lengths_before[-1][i]
        self.lengths_before.insert(self.inverse_permutation[-1] + 1, self.lengths_before[-1])
        self.permutation.insert(self.inverse_permutation[-1] + 1, self.permutation[-1])

        self.lengths_before.pop()
        self.permutation.pop()

        self.set_via_permutation(self.permutation, self.lengths_before)

    def right_step_when_image_is_smaller(self):
        for i in range(3):
            self.lengths_after[self.permutation[-1]][i] -= self.lengths_after[-1][i]
        self.lengths_after.insert(self.permutation[-1] + 1, self.lengths_after[-1])
        self.inverse_permutation.insert(self.permutation[-1] + 1, self.inverse_permutation[-1])

        self.lengths_after.pop()
        self.inverse_permutation.pop()

        self.set_via_inverse_permutation(self.inverse_permutation, self.lengths_after)

    def left_step_when_origin_is_smaller(self):
        for i in range(3):
            self.lengths_before[self.inverse_permutation[1]][i] -= self.lengths_before[1][i]
        self.lengths_before.insert(self.inverse_permutation[1], self.lengths_before[1])
        self.permutation.insert(self.inverse_permutation[1], self.permutation[1])

        del self.permutation[1]
        del self.lengths_before[1]

        self.set_via_permutation(self.permutation, self.lengths_before)

    def left_step_when_image_is_smaller(self):
        for i in range(3):
            self.lengths_after[self.permutation[1]][i] -= self.lengths_after[1][i]
        self.lengths_after.insert(self.permutation[1], self.lengths_after[1])
        self.inverse_permutation.insert(self.permutation[1], self.inverse_permutation[1])

        del self.inverse_permutation[1]
        del self.lengths_after[1]

        self.set_via_inverse_permutation(self.inverse_permutation, self.lengths_after)

    def right_step_of_Rauzy_induction(self):
        x = 1.8392867552141607
        # заменить на нормальное вычитание списков
        lengths_list = []
        for i in range(3):
            lengths_list.append(self.lengths_after[-1][i] - self.lengths_before[-1][i])

        length = lengths_list[0] + lengths_list[1]*x + lengths_list[2]*x**2
        if length < 0:
            self.right_step_when_image_is_smaller()
        else:
            self.right_step_when_origin_is_smaller()

    def left_step_of_Rauzy_induction(self):
        # тут пока идет сравнение через знак меньше, потом нужно будет определить
        # функцию smaller(first, second)
        x = 1.8392867552141607

        lengths_list = []
        for i in range(3):
            lengths_list.append(self.lengths_after[1][i] - self.lengths_before[1][i])

        length = lengths_list[0] + lengths_list[1]*x + lengths_list[2]*x**2
        if length < 0:
            self.left_step_when_image_is_smaller()
        else:
            self.left_step_when_origin_is_smaller()
        # если длины одинаковые, то нехорошо, пока что видимо у меня появляются куски нулевой длины
        # в принципе, это неинтересный случай, но надо все равно его обработать


# мне все меньше нравится приравнивание листов, надо заменить на копирование

# тестирование псевдопараметрических ПРАВЫХ шагов индукции
"""
T = IET()
lengths_before = [[0, 0, 0], [1, 1, 0], [0, -1, 1], [0, 1, 0], [-1, 1, 0], [0, -1, 1], [0, 1, 0], [1, 0, 0]]
# all lengths of format [k0, k1, k2] where length is equal to k0+k1*x+k2*x^2
T.set_via_permutation([0, 5, 1, 6, 3, 7, 4, 2], lengths_before)
T.right_step_of_Rauzy_induction()
T.right_step_of_Rauzy_induction()
T.right_step_of_Rauzy_induction()
print(T.lengths_before)
print(T.lengths_after)
print(T.permutation)
"""

# надо запустить шагов так 100 индукции (ПРАВОЙ) и повыводить перестановки

T = IET()
lengths_before = [[0, 0, 0], [1, 1, 0], [0, -1, 1], [0, 1, 0], [-1, 1, 0], [0, -1, 1], [0, 1, 0], [1, 0, 0]]
# all lengths of format [k0, k1, k2] where length is equal to k0+k1*x+k2*x^2
T.set_via_permutation([0, 5, 1, 6, 3, 7, 4, 2], lengths_before)

# это проверка на зацикливание, ВРОДЕ да, но надо найти коэффициент (на первых двух кусках проверен коэффициент x^(-3)
"""
for i in range(50):
    if i==27 or i==48:
        print(i, "    ", end='')
        print(T.permutation)
        print(T.lengths_before)
        print()
    T.right_step_of_Rauzy_induction()

"""
# в результате следующей беглой сверки с 4курсом циклы ТОЧНО имеют одинаковую длину и ВРОДЕ одинаковую структуру
# (первые 3-4 шага из 21 точно)
"""
for i in range(50):
    print(T.permutation)
    T.right_step_of_Rauzy_induction()
"""


# надо потестировать ЛЕВУЮ индукцию

# надо шесть раз обрезать ЛЕВОЙ индукцией и позапускать правую
