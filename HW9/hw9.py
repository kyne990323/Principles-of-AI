import numpy as np
import random
# 9.4.a
a1 = np.loadtxt('prob_a1.txt')
a2 = np.loadtxt('prob_a2.txt')
a3 = np.loadtxt('prob_a3.txt')
a4 = np.loadtxt('prob_a4.txt')

gamma = 0.9925

def construct(matrix):
    S = 81
    res = np.zeros((S, S))
    for i in range(matrix.shape[0]):
        res[int(matrix[i][0] - 1)][int(matrix[i][1] - 1)] = matrix[i][2]
    return res

trans1 = construct(a1)
trans2 = construct(a2)
trans3 = construct(a3)
trans4 = construct(a4)

state = list(range(1, 5))

trans = {}
for i in range(4):
    trans[i + 1] = eval('trans' + str(i + 1))

reward = np.loadtxt('rewards.txt')


def p_matrix(pol):
    S = 81
    res = np.zeros((S, S))
    for i in range(res.shape[0]):
        d = pol[i]
        prob = trans[d]
        res[i] = prob[i]
    return res

def v_matrix(p):
    I = np.eye(81)
    return np.matmul(np.linalg.inv(I - gamma * p), reward)

def q_matrix(v, state, action):
    sum = 0
    prob = trans[action]
    for i in range(81):
        sum += prob[state][i] * v[i]
    return reward[state] + gamma * sum

def update(v):
    res = np.zeros(81)
    for i in range(81):
        choice = []
        for j in range(1, 5):
            choice.append(q_matrix(v, i, j))
        res[i] = np.argmax(np.array(choice)) + 1
    return res


policy = np.zeros(81)
# 1 left 2 up 3 right 4 down
for i in range(len(policy)):
    direction = random.randint(1, 4)
    policy[i] = direction
for i in range(100):
    prev = np.copy(policy)
    P = p_matrix(policy)
    V = v_matrix(P)
    policy = update(V)
    if np.allclose(prev, policy): break

dir_res = ['\u25A0'] * 81
for i in range(len(policy)):
    if V[i] == 0:
        dir_res[i] = '\u25A0'
        continue
    if policy[i] == 1:
        dir_res[i] = '\u2190'
    elif policy[i] == 2:
        dir_res[i] = '\u2191'
    elif policy[i] == 3:
        dir_res[i] = '\u2192'
    else:
        dir_res[i] = '\u2193'
dragon = [46, 48, 50, 64, 66, 68]
for i in dragon:
    dir_res[i] = '\u2573'
dir_res = np.array(dir_res)
dir_res1 = dir_res.reshape((9, 9)).T
print(dir_res1)
V1 = np.around(V, 2)
print(V1.reshape((9, 9)).T)

# 9.4.b

def update_v(prev):
    res = np.zeros(81)
    for s in range(len(prev)):
        choice = []
        for i in range(1, 5):
            sum = 0
            for j in range(len(prev)):
                prob = trans[i]
                sum += prob[s][j] * prev[j]
            choice.append(reward[s] + gamma * sum)
        maximum = np.max(np.array(choice))
        res[s] = maximum
    return res

V_value = np.zeros(81)
counter = 0
while True:
    prev = np.copy(V_value)
    V_value = update_v(V_value)
    if counter > 50 and 0.001 > prev[2] - V_value[2] > -0.001:
        break
    counter += 1
policy_value = update(V_value) # same as part a
V_value = np.around(V_value, 2)
print(V_value.reshape((9, 9)).T)
dir_res2 = ['\u25A0'] * 81
for i in range(len(policy_value)):
    if V[i] == 0:
        dir_res2[i] = '\u25A0'
        continue
    if policy_value[i] == 1:
        dir_res2[i] = '\u2190'
    elif policy_value[i] == 2:
        dir_res2[i] = '\u2191'
    elif policy_value[i] == 3:
        dir_res2[i] = '\u2192'
    else:
        dir_res2[i] = '\u2193'
dragon = [46, 48, 50, 64, 66, 68]
for i in dragon:
    dir_res2[i] = '\u2573'
dir_res2 = np.array(dir_res2)
dir_res3 = dir_res2.reshape((9, 9)).T
print(dir_res3)