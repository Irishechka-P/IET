"""
Here l^3 = 5 l^2 + l + 1

<-
+
<-
<-
+
+
<-

Добавлена автоматическое сравнение циклов ВНУТРИ одной группы из 7 штук
На функцию маны не хватило, надо бы запихнуть, а то ЧЕРТ НОГУ СЛОМИТ...
На сравнение двух групп тоже маны не хватило, но сравнивать две штуки с двумя уже приятнее чем семь с семью

Пока у (x, y, z) -> (x, y, z) для (a, b, c) и (a+b+c, b, c) получается всегда две группы по три цикла ОДИНАКОВОЙ ДЛИНЫ,
     у (x, y, z) -> (x, z, y)                                                 две группа по три цикла РАЗНОЙ длины


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
        x = 5.22787141193659
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
        x = 5.22787141193659

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


def check_proportion(first_list_of_lengths, second_list_of_lengths, third_degree):
    """

    :param first_list_of_lengths: [1, 0, 1] means 1 + x^2. This is the list of such a lists (from 0 to 6).
    :param second_list_of_lengths:  [-1, 1, 0] means x - 1. --//--
    :param third_degree: [1, 1, 1] means expression x^3 = 1 + x + x^2
    :return: TRUE if first_list_of_lengths is proportional to second one, FALSE otherwise


    Example:
    third degree = [1, 1, 1]
    (1 + x^2) * (x - x^2) = -2x^2
    (x^2 - x) * (x - x^2) = 1 - x^2
    So [[1, 0, 1], [0, -1, 1]] is proportional to [[0, 0, -2], [1, 0, -1]]
    (with coefficient x - x^2, but it remains unknown)

    Process: checking if (1 + x^2) * (1) = (1 + 3x + 2x^2) * (x^2 - x)
    (6 equations)
    """
    a = first_list_of_lengths[1].copy()
    b = second_list_of_lengths[1].copy()
    for i in range(2, len(first_list_of_lengths)):
        c = first_list_of_lengths[i].copy()
        d = second_list_of_lengths[i].copy()

        # check a/c = b/d, i.e. a*d = b*c
        product_ad = []
        product_bc = []
        for j in range(5):
            ans_ad = 0
            ans_bc = 0
            # j is degree of variable in product
            for k1 in range(j + 1):
                k2 = j - k1
                if (k1 < 3) and (k2 < 3):
                    ans_ad += a[k1] * d[k2]
                    ans_bc += b[k1] * c[k2]
            product_ad.append(ans_ad)
            product_bc.append(ans_bc)
        """
        now we have product_ad = [x0, x1, x2, x3, x4] and
                    product_bc = [y0, y1, y2, y3, y4]
        we should bring both to the form [?, ?, ?, 0, 0] using THIRD_DEGREE
        """
        for k in (1, 2, 3):
            product_ad[k] += product_ad[4] * third_degree[k - 1]
            product_bc[k] += product_bc[4] * third_degree[k - 1]
        for k in (0, 1, 2):
            product_ad[k] += product_ad[3] * third_degree[k]
            product_bc[k] += product_bc[3] * third_degree[k]
        for k in range(3):
            if product_ad[k] != product_bc[k]:
                return False

    return True


def get_the_structure_of_cycle(T, kit):
    S = IET()
    S.set_via_permutation(T.permutation, T.lengths_before)
    kit['list of permutations'] = []
    kit['list of lists of lengths'] = []
    t = False

    while not t:
        # print("\t", S.lengths_before, "\t", S.permutation)
        permutation = S.permutation.copy()  # тут-то я и проштрафился (с) (но уже исправила, все нормально)
        list_of_lengths = []
        for i in range(8):
            list_of_lengths.append(S.lengths_before[i].copy())
        kit['list of permutations'].append(permutation)
        kit['list of lists of lengths'].append(list_of_lengths)
        """
        print(1, *kit['list of permutations'])
        print(2, *kit['list of lists of lengths'])
        print()
        """
        length = len(kit['list of permutations'])
        # print('\t', length)
        for i in range(1, length // 2 + 1):
            if (kit['list of permutations'][length - i: length] == kit['list of permutations'][length - 2 * i: length - i]) and (check_proportion(kit['list of lists of lengths'][length - i].copy(), kit['list of lists of lengths'][length - 2*i].copy(), [1, 1, 5])):
                kit['start'] = length - 2 * i
                kit['cycle'] = kit['list of permutations'][length - i: length]
                kit['length of cycle'] = i
                t = True
                break
        # print(S.permutation)
        S.right_step_of_Rauzy_induction()


T = IET()
# for (x,y,z) -> (x,z,y)
"""
# (a+b+c,b,c)  44444444444444
lengths_before = [[0, 0, 0], [0, 6, 0], [0, -3, 3], [0, -9, 3], [-3, 3, 0], [-3, 3, 0], [-3, 3, 0], [6, 0, 0]]
T.set_via_permutation([0, 3, 1, 6, 4, 2, 7, 5], lengths_before)
# two triplets, one with cycle length 70, another with cycle length 57 (такие же как в 333333333)
"""

"""
# (a, b, c)  3333333333333
lengths_before = [[0, 0, 0], [3, 18, -3], [0, -15, 3], [0, -9, 3], [-3, 3, 0], [-3, 3, 0], [-3, 3, 0], [6, 0, 0]]
T.set_via_permutation([0, 3, 1, 6, 4, 2, 7, 5], lengths_before)
# two triplets, one with cycle length 70, another with cycle length 57
"""

# for (x,y,z) -> (x,y,z)
"""
# (a+b+c, b, c) 111111
lengths_before = [[0, 0, 0], [0, 6, 0], [3, -6, 3], [-3, 3, 0], [-3, -6, 3], [-3, 3, 0], [-3, 3, 0], [6, 0, 0]]
T.set_via_permutation([0, 4, 1, 5, 7, 3, 2, 6], lengths_before)
# two triplets, both with cycle length 65
"""


# (a, b, c)   222222222
lengths_before = [[0, 0, 0], [6, 0, 0], [-3, 3, 0], [-3, -6, 3], [-3, 3, 0], [-3, 18, -3], [0, -15, 3], [6, 0, 0]]
T.set_via_permutation([0, 3, 5, 7, 2, 4, 1, 6], lengths_before)
# two triplets, both with cycle length 65, the same as in the (a+b+c,b,c)-case

list_of_summary_lengths = T.get_sums_of_len().copy()

s = list()

distinct_cycles = {}

# для отладки 1 для работы 7
for j in range(7):
    while T.get_sum_len() != list_of_summary_lengths[j]:
        T.left_step_of_Rauzy_induction()
    s.append({})
    get_the_structure_of_cycle(T, s[j])
    # print(s[j]['start'], s[j]['length of cycle'], *s[j]['cycle'], sep='\n')

    # дальше неотлаженная особо часть и ее еще надо в функцию запихать
    cc = []
    for perm in s[j]['cycle']:
        cc.append(tuple(perm))

    current_cycle = tuple(cc)
    f = 0
    for cyc in distinct_cycles:
        cycle = list(cyc)
        for i in range(len(cycle)):
            shifted_cycle = cycle[i:len(cycle)] + cycle[0: i]
            # print(tuple(shifted_cycle), current_cycle, sep='\n')
            # print()
            if tuple(shifted_cycle) == current_cycle:
                distinct_cycles[cyc] += 1
                f = 1
    if f == 0:
        distinct_cycles[current_cycle] = 1

for key in distinct_cycles:
    print(distinct_cycles[key], len(key), *key, sep='\n')

# print(s[j]['start'], s[j]['length of cycle'], *s[j]['cycle'], *s[j]['list of lists of lengths'], sep='\n')
# print(s[j]['start'], s[j]['length of cycle'], sep=', ')
