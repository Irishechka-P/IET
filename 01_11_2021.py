"""
(a, b, c) - параметры из 4-курсовой
По ним (ручками) построен братишка для initial с параметрами (a+b+c, b, c). Тут играемся с ним.
А именно, получаем структуру его циклов.
ДЛЯ АВТОМАТИЧНОСТИ НЕ ХВАТАЕТ РАЗБИЕНИЯ ПОЛУЧЕННЫХ ЦИКЛОВ НА КЛАССЫ ЭКВИВАЛЕНТНОСТИ.
Структура для самого (a, b, c) записана в курсовой. Сверяем пока что тоже вручную...

Не знаю, стоит ли добавлять проверку пропорциональности, все равно скрипт ПСЕВДОпараметрический. Ну для себя можно.

Еще хорошо бы подумать, как < заменить на is_smaller, но это уже для гениев.
"""


class IET:
    def __init__(self):
        self.permutation = [0, 1]
        self.inverse_permutation = [0, 1]
        self.lengths_before = [0, 1]
        self.lengths_after = [0, 1]

    def get_sum_len(self):
        answer = [0, 0, 0]
        for i in range(len(self.lengths_before)):
            for j in range(3):
                answer[j] += self.lengths_before[i][j]
        return answer

    def get_sums_of_len(self):
        """
        It's necessary for getting 6 other IETs for initial one.
        Applying left_step_of_Rauzy to T until sum_len(T) equals sums_of_len[0] we'll get 1st;
                                                                 sums_of_len[1] we'll get 2nd;
        and so on.

        """
        answer = list()
        answer.append(self.get_sum_len().copy())

        for j in range(1, 7):
            answer.append(answer[-1].copy())
            for i in range(3):
                answer[-1][i] -= self.lengths_before[j][i]
        return answer

    def set_via_permutation(self, permutation, lengths_before):
        # set IET via _permutation_ and _lengths_before_
        # supposed that len(_permutation_) == len(_lengths_before_)
        # perhaps improve later
        # always supposed that _permutation_ IS A PERMUTATION
        self.permutation = permutation.copy()
        self.lengths_before = []
        for param_len in lengths_before:
            self.lengths_before.append(param_len.copy())

        self.inverse_permutation = [0] * len(self.permutation)
        self.lengths_after = [0] * len(self.permutation)

        for i in range(len(self.permutation)):
            self.inverse_permutation[self.permutation[i]] = i
            self.lengths_after[self.permutation[i]] = self.lengths_before[i]

    def set_via_inverse_permutation(self, inverse_permutation, lengths_after):
        self.inverse_permutation = inverse_permutation.copy()
        self.lengths_after = []
        for param_len in lengths_after:
            self.lengths_after.append(param_len.copy())

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

        length = lengths_list[0] + lengths_list[1] * x + lengths_list[2] * x ** 2
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

        length = lengths_list[0] + lengths_list[1] * x + lengths_list[2] * x ** 2
        if length < 0:
            self.left_step_when_image_is_smaller()
        else:
            self.left_step_when_origin_is_smaller()
        # если длины одинаковые, то нехорошо, пока что видимо у меня появляются куски нулевой длины
        # в принципе, это неинтересный случай, но надо все равно его обработать


def get_the_structure_of_cycle(T, kit):
    S = IET()
    S.set_via_permutation(T.permutation, T.lengths_before)
    kit['list of permutations'] = []
    t = False

    while not t:
        permutation = S.permutation.copy()  # тут-то я и проштрафился (с) (но уже исправила, все нормально)
        kit['list of permutations'].append(permutation)
        length = len(kit['list of permutations'])
        for i in range(1, length // 2 + 1):
            if kit['list of permutations'][length - i: length] == kit['list of permutations'][length - 2 * i: length - i]:
                kit['start'] = length - 2 * i
                kit['cycle'] = kit['list of permutations'][length - i: length]
                kit['length of cycle'] = i
                t = True
                break
        S.right_step_of_Rauzy_induction()


T = IET()
lengths_before = [[0, 0, 0], [1, 1, 0], [0, -1, 1], [0, 1, 0], [-1, 1, 0], [0, -1, 1], [0, 1, 0], [1, 0, 0]]
# all lengths of format [k0, k1, k2] where length is equal to k0+k1*x+k2*x^2
T.set_via_permutation([0, 5, 1, 6, 3, 7, 4, 2], lengths_before)

list_of_summary_lengths = T.get_sums_of_len().copy()
# print(list_of_summary_lengths)

s = list()

for j in range(7):
    while T.get_sum_len() != list_of_summary_lengths[j]:
        T.left_step_of_Rauzy_induction()
    s.append({})
    get_the_structure_of_cycle(T, s[j])
    print(s[j]['start'], s[j]['length of cycle'], *s[j]['cycle'], sep='\n')
    # print(s[j]['start'], s[j]['length of cycle'], sep=', ')

# надо потестировать ЛЕВУЮ индукцию
# надо шесть раз обрезать ЛЕВОЙ индукцией и позапускать правую
# ожидается, что везде будут циклы длины 21, структуры будет две различных (две группы по 3)
# получилось именно так, чего НЕ МОГЛО произойти случайно, так что тестировать левую индукцию мы КОНЕЧНО ЖЕ не будем.
