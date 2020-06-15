from itertools import product
import numpy as np


def nonlin(x, deriv=False):     # sigmoid func maps any value bet ween zero and 1
    if deriv:
        return x*(1-x)
    return 1/(1+np.exp(-x))


def training():
    x = list(product([0, 1], repeat=3))[:-1]
    x = [list(i) for i in x]

    # insert boundaries and bias
    for i in range(len(x)):
        x[i].append(1)  # right boundary
        x[i].insert(0, 1)  # left boundary
    for each in x:
        each.append(1)  # insert bias

    x_l = len(x)
    # insert car_pos
    for i in range(3):
        for j in range(x_l):
            data = list(x[j])
            data.append(i / 2.0)
            x.append(data)

    x = x[x_l:]
    x = np.array(x)
    y = [[0.1], [0.1], [0.1], [0.1], [0.2], [0.2], [0.4], [0.1], [0.1], [0.3], [0.3], [0.1], [0.1], [0.2], [0.1], [0.3], [0.1], [0.5], [0.1], [0.3], [0.1]]
    y = np.array(y)

    syn0 = 2*np.random.random((7, 5)) - 1       # joins with random weight
    syn1 = 2*np.random.random((5, 1)) - 1

    # training step
    for i in range(100000):
        l0 = x
        l1 = nonlin(np.dot(l0, syn0))
        l2 = nonlin(np.dot(l1, syn1))

        # compare error

        l2_error = y - l2
        # if np.mean(np.abs(l2_error)) < 0.01:
        #     break
        if i % 20000 == 0:
            print("Error:"+str(np.mean(np.abs(l2_error))))

        l2_delta = l2_error*nonlin(l2, deriv=True)

        # backpropogating to check how much did l1 contribute to error
        l1_error = l2_delta.dot(syn1.T) # weights in 1 transpose
        l1_delta = l1_error * nonlin(l1, deriv=True)

        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)

    return syn0, syn1


def predict(model_input, test_data):
    l0 = test_data
    l1 = nonlin(np.dot(l0, model_input[0]))
    l2 = nonlin(np.dot(l1, model_input[1]))
    return round((l2[0][0]), 1)


# obj = training()
# z = [[1, 0, 1, 1, 1, 1, 1.0]]
# test = np.array(z)
# print(test)
# print(predict(obj, test))