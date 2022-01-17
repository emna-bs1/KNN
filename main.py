import csv
from statistics import mean
import random
from math import sqrt

min_col = []
max_col = []
normalized = []
counter = 0


def check_if_number(element):
    try:
        float(element)
        return True
    except ValueError:
        return False


with open('Heart_Disease.csv', encoding='utf-8-sig') as heart_info:
    reader = csv.reader(heart_info, delimiter=',')
    columns = list(zip(*reader))

    for col_ind in range(len(columns) - 1):
        filtered = list(filter(check_if_number, columns[col_ind]))
        if len(filtered) != len(columns[col_ind]):
            print(columns[col_ind])
            filtered = list(map(lambda x: float(x), filtered))
            columns[col_ind] = tuple(','.join(columns[col_ind]).replace('?', str(mean(filtered))).split(','))
        columns[col_ind] = tuple(map(lambda x: float(x), columns[col_ind]))

        min_col.append(min(columns[col_ind]))
        max_col.append(max(columns[col_ind]))

        res = [*columns[col_ind]]
        denominator = max_col[col_ind]
        denominator -= min_col[col_ind]

        normalized.append(tuple(map(lambda x: (x - min_col[col_ind]) / denominator, res)))
    normalized.append(columns[len(columns) - 1])

print(min_col)
print(max_col)
print(normalized)


def split_list(to_split):
    training_percentage = int(len(to_split) * 0.7)
    print(training_percentage)
    random.shuffle(to_split)
    return to_split[:training_percentage], to_split[training_percentage:]


training_set, test_set = split_list(list(map(tuple, zip(*normalized))))
print(training_set, test_set)


def k_min(distances, k_val):
    k_mins_target = []
    dis = [elem[0] for elem in distances]
    for ind in range(k_val):
        min_l = min(dis)
        k_mins_target.append(distances[dis.index(min_l)][1])
        dis.remove(min_l)
    return k_mins_target


def result(t):
    elements = set(t)
    occ = dict()
    for element in elements:
        occ[element] = t.count(element)
    print(occ)
    max_count = max(occ.values())
    '''print(max(occ, key=occ.get))'''
    values = [key for key, value in occ.items() if value == max_count]
    return values


def knn(training_s, distance_type, k_val, test):
    distances = []
    for row_ind in range(len(training_s)):
        distance_calc = 0
        for col_index in range(len(test) - 1):
            if distance_type == 1:
                distance_calc += abs(training_s[row_ind][col_index] - test[col_index])
            else:
                distance_calc += (training_s[row_ind][col_ind] - test[col_index]) ** 2
        if distance_type == 2:
            distance_calc = sqrt(distance_calc)
        distances.append((distance_calc, training_s[row_ind][len(test) - 1]))

    print(len(distances))
    print(distances)
    target = k_min(distances, k_val)
    print(target)

    res_tar = result(target)
    if len(res_tar) > 1:
        print("could not predict, more than one possibility was found ", *res_tar, sep=',')
    else:
        print("prediction: ", *res_tar)

    print("result has to be: ", test[len(test) - 1])


while 1:
    print("----- KNN -----")

    print("test set: ")
    pick_element = random.choice(test_set)
    for (i, item) in enumerate(test_set, start=1):
        print(i, item)

    while 1:
        pick_elem_choice = input("pick element from test set randomly: press r\n"
                                 "enter element's index: \n")
        try:
            pick_elem_choice = int(pick_elem_choice)
            assert pick_elem_choice in range(1, len(test_set) + 1)
            pick_element = test_set[pick_elem_choice - 1]
            break
        except ValueError:
            if pick_elem_choice.lower() == 'r':
                break
            print("invalid choice")
            continue
        except AssertionError:
            print("no element corresponding to entered index was found")
            continue

    print("chosen element: ", pick_element)
    k = int(input("k value: "))
    while 1:
        try:
            distance = int(input("1/ Manhattan distance\n2/ Euclidean distance\n"))
            assert distance in [1, 2]
            break
        except ValueError:
            print("your choice has to be of type number")
        except AssertionError:
            print("please enter a valid choice")

    knn(training_set, distance, k, pick_element)
    try:
        pursue = input("press q or 0 if you want to stop\n")
        assert pursue.lower() in ['q', '0']
        break
    except AssertionError:
        continue
