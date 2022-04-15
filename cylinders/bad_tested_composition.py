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

        positions = [(numbered_numerical_partition_after[j][0], j + 1)
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

    @staticmethod
    def composition(T0, S0):
        T = IET()
        S = IET()
        R = IET()
        numb_part_before = []
        numb_part_after = []

        T.set_via_permutation(permutation=T0.permutation,
                              lengths_before=T0.lengths_before)
        S.set_via_permutation(permutation=S0.permutation,
                              lengths_before=S0.lengths_before)

        i = 1  # номер кусочка на котором стоим
        # общий ли он для прохода по S и T или надо заводить два разных
        while i < len(S.numerical_lengths_before):
            if S.numerical_lengths_before[i] > T.numerical_lengths_after[i]:
                S.lengths_before.insert(i + 1,
                                        list(np.asarray(S.lengths_before[i]) -
                                             np.asarray(T.lengths_after[i])))
                S.lengths_before[i] = copy.copy(T.lengths_after[i])
                critical_index = S.permutation[i]
                permutation = np.asarray(S.permutation)
                permutation[permutation > critical_index] += 1
                S.permutation = list(permutation)
                S.permutation.insert(i + 1, critical_index + 1)

                S.set_via_permutation(S.permutation, S.lengths_before)

            if S.numerical_lengths_before[i] < T.numerical_lengths_after[i]:
                T.lengths_after.insert(i + 1,
                                       list(np.asarray(T.lengths_after[i]) -
                                            np.asarray(S.lengths_before[i])))
                T.lengths_after[i] = copy.copy(S.lengths_before[i])

                inv_permutation = np.asarray(T.inverse_permutation)
                critical_index = inv_permutation[i]
                inv_permutation[inv_permutation > critical_index] += 1
                T.inverse_permutation = list(inv_permutation)
                T.inverse_permutation.insert(i + 1, critical_index + 1)

                T.set_via_inverse_permutation(T.inverse_permutation, T.lengths_after)

            # на этом моменте i-тый кусок в T-after равен i-тому куску в S-before
            part_before_element = copy.copy(T.partition_before[T.inverse_permutation[i] - 1])
            numb_part_before.append((i, part_before_element))

            # print(S.partition_after)
            # print()
            part_after_element = copy.copy(S.partition_after[S.permutation[i] - 1])
            numb_part_after.append((i, part_after_element))

            i += 1

        # print(numb_part_before, numb_part_after, sep='\n')
        R.set_via_numbered_partitions(numb_part_before, numb_part_after)

        return R


ALPHA = [1, 0.61, 0.24, 0.15]
N_params = 4
SUM_params = [0, 1, 1, 1]

lengths_before_test1 = [[0, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                        ]
permutation_test1 = [0, 3, 2, 1]

T = IET()

T.set_via_permutation(permutation_test1, lengths_before_test1)


lengths_before_test2 = [[0, 0, 0, 0],
                        [0, 1, -1, 0],
                        [0, 0, 1, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                        ]
permutation_test2 = [0, 4, 1, 3, 2]


S = IET()

S.set_via_permutation(permutation_test2, lengths_before_test2)

"""
print(T.lengths_before)
print(T.numerical_lengths_before)
print(T.permutation)
print()
print(S.lengths_before)
print(S.numerical_lengths_before)
print(S.permutation)
print()
"""
R = IET.composition(T, S)
print(R.lengths_before)
print(R.permutation)
