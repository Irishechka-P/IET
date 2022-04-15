import numpy as np
import copy


class IET:
    global ALPHA
    global N_params
    global SUM_params

    def __init__(self):
        self.lengths_before = []
        self.lengths_after = []

        self.partition_before = []
        self.partition_after = []

        self.permutation = []
        self.inverse_permutation = []

        self.numerical_lengths_before = []
        self.numerical_lengths_after = []

        self.numerical_partition_before = []
        self.numerical_partition_after = []

    def set_via_permutation(self, permutation, lengths_before):
        self.lengths_before = copy.deepcopy(lengths_before)
        self.lengths_after = [0] * len(permutation)

        self.permutation = copy.copy(permutation)
        self.inverse_permutation = [0] * len(permutation)

        for i in range(len(permutation)):
            self.inverse_permutation[permutation[i]] = i
            self.lengths_after[permutation[i]] = copy.copy(lengths_before[i])

        self.partition_before = np.apply_along_axis(np.cumsum, 0, self.lengths_before)
        self.partition_after = np.apply_along_axis(np.cumsum, 0, self.lengths_after)

        self.numerical_lengths_before = [sum([ALPHA[i] * self.lengths_before[j][i]
                                              for i in range(N_params)])
                                         for j in range(len(self.lengths_before))]

        self.numerical_lengths_after = [sum([ALPHA[i] * self.lengths_after[j][i]
                                             for i in range(N_params)])
                                        for j in range(len(self.lengths_after))]

        self.numerical_partition_before = np.cumsum(self.numerical_lengths_before)
        self.numerical_partition_after = np.cumsum(self.numerical_lengths_after)

    def set_via_inverse_permutation(self, inverse_permutation, lengths_after):
        self.lengths_after = copy.deepcopy(lengths_after)
        self.lengths_before = [0] * len(inverse_permutation)

        self.inverse_permutation = copy.copy(inverse_permutation)
        self.permutation = [0] * len(inverse_permutation)

        for i in range(len(inverse_permutation)):
            self.permutation[inverse_permutation[i]] = i
            self.lengths_before[inverse_permutation[i]] = copy.copy(lengths_after[i])

        self.partition_before = np.apply_along_axis(np.cumsum, 0, self.lengths_before)
        self.partition_after = np.apply_along_axis(np.cumsum, 0, self.lengths_after)

        self.numerical_lengths_before = [sum([ALPHA[i] * self.lengths_before[j][i]
                                              for i in range(N_params)])
                                         for j in range(len(self.lengths_before))]

        self.numerical_lengths_after = [sum([ALPHA[i] * self.lengths_after[j][i]
                                             for i in range(N_params)])
                                        for j in range(len(self.lengths_after))]

        self.numerical_partition_before = np.cumsum(self.numerical_lengths_before)
        self.numerical_partition_after = np.cumsum(self.numerical_lengths_after)

    def set_via_numbered_partitions(self,
                                    numbered_partition_before,
                                    numbered_partition_after):
        # print(self.lengths_after)
        # print(numbered_partition_before)
        numbered_numerical_partition_before = [(number,
                                                sum([ALPHA[j] * point[j] for j in range(N_params)]),
                                                copy.copy(point))
                                               for number, point in numbered_partition_before]
        numbered_numerical_partition_before.sort(key=lambda triplet: triplet[1])
        # print(numbered_numerical_partition_before)

        # print(numbered_partition_after)
        numbered_numerical_partition_after = [(number,
                                               sum([ALPHA[j] * point[j] for j in range(N_params)]),
                                               copy.copy(point))
                                              for number, point in numbered_partition_after]
        numbered_numerical_partition_after.sort(key=lambda triplet: triplet[1])
        # print(numbered_numerical_partition_after)

        positions = [(numbered_numerical_partition_after[j][0], j+1)
                     for j in range(len(numbered_numerical_partition_after))]
        positions.sort(key=lambda pair: pair[0])
        # print(positions)

        self.lengths_before.append([0] * N_params)
        self.permutation.append(0)
        for i in range(len(numbered_numerical_partition_before) - 1):
            self.lengths_before.append(list(np.asarray(numbered_numerical_partition_before[i + 1][-1]) -
                                       np.asarray(numbered_numerical_partition_before[i][-1])))
            self.permutation.append(positions[numbered_numerical_partition_before[i][0] - 1][1])
        self.lengths_before.append(list(np.asarray(SUM_params) -
                                   np.asarray(numbered_numerical_partition_before[-1][-1])))
        self.permutation.append(
            positions[numbered_numerical_partition_before[len(numbered_numerical_partition_before) - 1][0] - 1][1])
        # print(self.lengths_before)
        # print(self.permutation)
        self.set_via_permutation(self.permutation, self.lengths_before)
        # print('I am here')
        # print(self.lengths_after)
        # print(self.inverse_permutation)


ALPHA = [1, 0.61, 0.24, 0.15]
N_params = 4
SUM_params = [0, 1, 1, 1]

S = IET()

"""
numbered_partition_before_1 = [(1, [0, 0, 0, 0]),
                              (2, [0, 0, 1, 2]),
                              (3, [0, 0, 0, 1])]
numbered_partition_after_1 = [(3, [0, 1, 0, -1]),
                             (1, [0, 1, 1, 0]),
                             (2, [0, 0, 0, 0])]
"""

"""
SUM_params = [0, 2, 2, -3]
numbered_partition_before_2 = [(3, [0, 0, 0, 0]),
                              (4, [0, 1, -1, 0]),
                              (1, [0, 1, -1, 1]),
                              (5, [0, 1, 0, 0]),
                              (2, [0, 1, 2, -3])]
numbered_partition_after_2 = [(2, [0, 0, 0, 0]),
                             (3, [0, 1, 0, 0]),
                             (1, [0, 2, -1, 0]),
                             (4, [0, 2, 0, -1]),
                             (5, [0, 2, 0, 0])]
# Слишком удачное было бы совпадение, если бы это работало случайно,
# так что считаем, что потестили

S.set_via_numbered_partitions(numbered_partition_before=numbered_partition_before_,
                              numbered_partition_after=numbered_partition_after_)
"""

ALPHA = [1, 0.61, 0.24, 0.15]

"""
lengths_before_ = [[0, 0, 0, 0],  # fictive segment
                   [0, 1, -1, 0],  # l1 - l2
                   [0, 0, 0, 1],  # l3
                   [0, 0, 1, -1],  # l2 - l3
                   [1, -2, 0, 0],  # 1 - 2*l1
                   [0, 0, 1, -1],  # l2 - l3
                   [0, 0, 0, 1],  # l3
                   [0, 1, -1, 0],  # l1 - l2
                   ]
permutation_ = [0, 5, 7, 2, 4, 6, 1, 3]

lengths_before_test = [[0, 0, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1],
                       [0, 1, -1, 1],
                       [0, 0, 1, -1]]
permutation_test = [0, 2, 1, 4, 3]

T = IET()
# T.set_via_permutation(permutation=permutation_, lengths_before=lengths_before_)

T.set_via_permutation(permutation=permutation_test, lengths_before=lengths_before_test)

print(T.permutation)
print(T.inverse_permutation)

print(f'{ALPHA=}')

print(T.lengths_before)
print(T.partition_before)
print()
print(T.numerical_lengths_before)
print(T.numerical_partition_before)
print()
print()
print(T.lengths_after)
print(T.partition_after)
print()
print(T.numerical_lengths_after)
print(T.numerical_partition_after)
"""
