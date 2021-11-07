"""
Тут рассматривается T2 из курсовой, т.е. (a,b,c) = (1, x, x^2) и порядок (a,c,b) справа.
Ну и потом соответственно T2', порядок тот же, параметры (1+x+x^2, x, x^2).
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
        # print("\t", S.lengths_before, "\t", S.permutation)
        permutation = S.permutation.copy()  # тут-то я и проштрафился (с) (но уже исправила, все нормально)
        kit['list of permutations'].append(permutation)
        length = len(kit['list of permutations'])
        # rint('\t', length)
        for i in range(20, length // 2 + 1):
            if kit['list of permutations'][length - i: length] == kit['list of permutations'][length - 2 * i: length - i]:
                kit['start'] = length - 2 * i
                kit['cycle'] = kit['list of permutations'][length - i: length]
                kit['length of cycle'] = i
                t = True
                break
        # print(S.permutation)
        S.right_step_of_Rauzy_induction()


"""
Ну вообще-то получается 3 по 21 и 4 по 25 в модифиц. и 4 по 21 и 3 по 25 в исходном
Надо убедиться что лишнее в модифиц. 25, а в исходном 21
и на самом деле и там и там два набора по три (21 и 25)
"""


"""
здесь тоже проверить пропорциональность
"""
T = IET()
# all lengths of format [k0, k1, k2] where length is equal to k0+k1*x+k2*x^2
lengths_before = [[0, 0, 0], [2, 1, -1], [-1, -1, 1], [-1, 1, 0], [0, -3, 2], [0, 2, -1], [0, 1, 0], [1, 0, 0]]
T.set_via_permutation([0, 3, 1, 7, 5, 4, 2, 6], lengths_before)
"""
# три цикла длины 21, три цикла длины 25. из-за костыля в get_structure_of_cycles вынуждена проверить пропорциональность!!!
lengths_before = [[0, 0, 0], [1, 1, 0], [0, 0, 1], [-1, 1, 0], [0, -3, 2], [0, 2, -1], [0, 1, 0], [1, 0, 0]]
T.set_via_permutation([0, 3, 1, 7, 5, 4, 2, 6], lengths_before)
"""
list_of_summary_lengths = T.get_sums_of_len().copy()
print(list_of_summary_lengths)

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
# ну при беглой сверке эти структуры совпали с тем, что есть в 4-курсовой, А ЧЕГО ЕЩЕ СЛЕДОВАЛО ОЖИДАТЬ
# получилось именно так, чего НЕ МОГЛО произойти случайно, так что тестировать левую индукцию мы КОНЕЧНО ЖЕ не будем.
