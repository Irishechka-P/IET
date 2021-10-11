class IET:
    def __init__(self, permutation=[0, 1], inverse_permutation=[0, 1], lengths_before=[0, 1], lengths_after=[0, 1]):
        self.permutation = permutation
        self.inverse_permutation = inverse_permutation
        self.lengths_before = lengths_before
        self.lengths_after = lengths_after

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

        # смутные подозрения, что параметрические подсчеты будет ОЧЕНЬ ЛЕГКО РЕАЛИЗОВАТЬ
        # просто lengths_before := [[k1_1,...,km_1], ... , [k1_n,...,km_n]]

###ТУТ ОШИБКА. К НЕКОТОРЫМ ЗНАЧЕНИЯМ SELF.PERMUTATION НАДО ПРИБАВИТЬ 1. ПОЧЕМУ Я ЕЕ НЕ ЗАМЕТИЛА??
    #ладно возможно ее нет...
    def right_step_when_origin_is_smaller(self):
        self.lengths_before[self.inverse_permutation[-1]] -= self.lengths_before[-1]
        self.lengths_before.insert(self.inverse_permutation[-1] + 1, self.lengths_before[-1])
        self.permutation.insert(self.inverse_permutation[-1] + 1, self.permutation[-1])
        self.lengths_before.pop()
        self.permutation.pop()
        # self.set_via_permutation(self.permutation, self.lengths_before):
        # что-то не прокатило так написать, ругается на синтаксис
        for i in range(len(self.permutation)):
            self.inverse_permutation[self.permutation[i]] = i
            self.lengths_after[self.permutation[i]] = self.lengths_before[i]

###ТУТ ОШИБКА. К НЕКОТОРЫМ ЗНАЧЕНИЯМ SELF.PERMUTATION НАДО ПРИБАВИТЬ 1. ПОЧЕМУ Я ЕЕ НЕ ЗАМЕТИЛА??
    def right_step_when_image_is_smaller(self):
        self.lengths_after[self.permutation[-1]] -= self.lengths_after[-1]
        self.lengths_after.insert(self.permutation[-1] + 1, self.lengths_after[-1])
        self.inverse_permutation.insert(self.permutation[-1] + 1, self.inverse_permutation[-1])

        self.lengths_after.pop()
        self.inverse_permutation.pop()

        # ДОПИСАТЬ set_via_inverse_permutation, если получится
        # и тогда заменить следующий код одним вызовом

        for i in range(len(self.inverse_permutation)):
            self.permutation[self.inverse_permutation[i]] = i
            self.lengths_before[self.inverse_permutation[i]] = self.lengths_after[i]



######################################################
###ЭТО ВООБЩЕ НЕ ТО ЧТО НУЖНО ПЕРЕПИСАТЬ ПОЛНОСТЬЮ
######################################################
    def left_step_when_origin_is_smaller(self):



        self.lengths_after[self.permutation[-1]] -= self.lengths_after[-1]
        self.lengths_after.insert(self.permutation[-1] + 1, self.lengths_after[-1])
        self.inverse_permutation.insert(self.permutation[-1] + 1, self.inverse_permutation[-1])

        self.lengths_after.pop()
        self.inverse_permutation.pop()

        # ДОПИСАТЬ set_via_inverse_permutation, если получится
        # и тогда заменить следующий код одним вызовом

        for i in range(len(self.inverse_permutation)):
            self.permutation[self.inverse_permutation[i]] = i
            self.lengths_before[self.inverse_permutation[i]] = self.lengths_after[i]



######################################################
###  ТЕСТИРОВАТЬ
######################################################
    def left_step_when_image_is_smaller(self):
        self.lengths_after[self.permutation[1]] -= self.lengths_after[1]
        self.lengths_after.insert(self.permutation[1], self.lengths_after[1])
        self.inverse_permutation.insert(self.permutation[1], self.inverse_permutation[1])

        del self.inverse_permutation[1]
        del self.lengths_after[1]

        # ДОПИСАТЬ set_via_inverse_permutation, если получится
        # и тогда заменить следующий код одним вызовом

        for i in range(len(self.inverse_permutation)):
            self.permutation[self.inverse_permutation[i]] = i
            self.lengths_before[self.inverse_permutation[i]] = self.lengths_after[i]

    def right_step_of_Rauzy_induction(self):
        # тут пока идет сравнение через знак меньше, потом нужно будет определить
        # функцию smaller(first, second)
        if self.lengths_after[-1] < self.lengths_before[-1]:
            self.right_step_when_image_is_smaller()

        else:
            self.right_step_when_origin_is_smaller()
        # если длины одинаковые, то нехорошо, пока что видимо у меня появляются куски нулевой длины
        # в принципе, это неинтересный случай, но надо все равно его обработать

    def left_step_of_Rauzy_induction(self):
        # тут пока идет сравнение через знак меньше, потом нужно будет определить
        # функцию smaller(first, second)
        if self.lengths_after[1] < self.lengths_before[1]:
            self.left_step_when_image_is_smaller()

        else:
            self.left_step_when_origin_is_smaller()
        # если длины одинаковые, то нехорошо, пока что видимо у меня появляются куски нулевой длины
        # в принципе, это неинтересный случай, но надо все равно его обработать



# тестирование шага индукции с origin.first<image.first
#ОТСУТСТВУЕТ КАК И РЕАЛИЗАЦИЯ ЭТОГО ШАГА!!!

# тестирование шага индукции с origin.first>image.first
"""
T = IET()
T.set_via_permutation([0, 3, 5, 1, 4, 2], [0, 2.5, 3.0, 2.0, 2.5, 5.0])

print(T.lengths_before)
print(T.lengths_after)

T.left_step_of_Rauzy_induction()
print()
print(T.lengths_before)
print(T.lengths_after)
print(T.permutation)
print(T.inverse_permutation)
"""

# тестировала каждый right_step на одном примере, что не есть хорошо, надо потестировать еще

# тестирование шага индукции с origin.last>image.last
"""
T = IET()
T.set_via_permutation([0, 3, 5, 1, 4, 2], [0, 2.5, 3.0, 2.0, 2.5, 5.0])

print(T.lengths_before)
print(T.lengths_after)

T.right_step_of_Rauzy_induction()
print()
print(T.lengths_before)
print(T.lengths_after)
print(T.permutation)
print(T.inverse_permutation)
"""
# тестирование шага индукции с origin.last<image.last
"""
T = IET()
T.set_via_permutation([0, 2, 4, 5, 1, 3], [0, 2.5, 1.5, 4.0, 2.0, 2.0])
print(T.lengths_before)
print(T.lengths_after)
T.step_of_Rauzy_induction()
print()
print(T.lengths_before)
print(T.lengths_after)
print(T.permutation)
print(T.inverse_permutation)"""

"""
T = IET([0, 2, 1], [0, 2, 1], [0, 0.4, 0.6], [0, 0.6, 0.4])
print(T.lengths_after)

S = IET()
print(S.permutation)
"""
