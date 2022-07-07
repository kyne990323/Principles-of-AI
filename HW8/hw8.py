import numpy as np

pid = []

with open("hw8_ids.txt", "r") as ids:
    for line in ids.readlines():
        pid.append(line[:-1])

movie = []
with open("hw8_movies.txt", "r") as mvs:
    for line in mvs.readlines():
        movie.append(line[:-1])

rating = []
with open("hw8_ratings.txt", "r") as rts:
    for line in rts.readlines():
        line = line.strip('\n')
        line = line.split(' ')
        rating.append(line)

rating = np.array(rating)
print(rating.shape)

index = {}
for i in range(rating.shape[1]):
    saw = 0
    rec = 0
    for j in range(rating.shape[0]):
        if rating[j][i] != '?':
            saw += 1
        if rating[j][i] == '1':
            rec += 1
    index[i] = rec / saw

index_sorted = sorted(index.items(), key=lambda x: x[1])
movie_sorted = []
for i in range(len(index_sorted)):
    movie_sorted.append(movie[index_sorted[i][0]])
print(movie_sorted)

# 8.1.e
probR = np.loadtxt("hw8_probR_init.txt")
probZ = np.loadtxt("hw8_probZ_init.txt").flatten()


# returns Omega_t
def seen(t) -> list:
    res = []
    for rate in rating[t]:
        if rate != '?':
            res.append(1)
        else:
            res.append(0)
    return res


# Z R are ndarray
def prior(Z, R, t):
    K = Z.shape[0]  # 4
    O_t = seen(t)
    J = len(movie)  # 76
    sum = 0

    for i in range(K):
        prod = 1
        for j in range(J):
            if O_t[j] == 0:
                continue
            r_jt = int(rating[t][j])
            if r_jt == 1:
                prod *= R[j][i]
            else:
                prod *= 1 - R[j][i]
        sum += Z[i] * prod
    return sum


def rou_it(Z, R, i, t):
    denom = prior(Z, R, t)
    prod = 1
    O_t = seen(t)
    J = len(movie)
    for j in range(J):
        if O_t[j] == 0:
            continue
        r_jt = int(rating[t][j])
        if r_jt == 1:
            prod *= R[j][i]
        else:
            prod *= 1 - R[j][i]
    num = Z[i] * prod
    return num / denom


def likelihood(Z, R):
    sum = 0
    T = len(pid)
    for t in range(T):
        sum += np.log(prior(Z, R, t))
    return sum / T


def update(Z, R, iter):
    res_Z = np.copy(Z)
    res_R = np.copy(R)
    K = Z.shape[0]  # 4

    T = len(pid)  # 362
    J = len(movie)  # 76

    for k in range(iter):  # 256
        if k in [0, 1, 2, 4, 8, 16, 32, 64, 128, 256]:
            print(k)
            ll = likelihood(res_Z, res_R)
            print(ll)

        # rou_it = rou_it_mat[t][i]
        rou_it_mat = np.zeros((362, 4))
        for t in range(362):
            for i in range(4):
                rou_it_mat[t][i] = rou_it(res_Z, res_R, i, t)

        # update P(Z=i)

        for i in range(K):  # 4
            sum = 0
            for t in range(T):
                sum += rou_it_mat[t][i]
            res_Z[i] = sum / T
        # Update P(R_j=1|Z=i)
        for j in range(J):  # 76
            for i in range(K):  # 4
                denom = 0
                for t in range(T):
                    denom += rou_it_mat[t][i]
                num = 0
                for t in range(T):  # 362
                    if seen(t)[j] == 1:
                        if int(rating[t][j]) == 1:
                            num += rou_it_mat[t][i]
                        else:
                            continue
                    else:
                        num += rou_it_mat[t][i] * res_R[j][i]
                res_R[j][i] = num / denom
    return res_Z, res_R


# takes about 10 minutes to run :(
final_Z, final_R = update(probZ, probR, 257)

prob = [0] * len(movie)
pid = np.array(pid)

row = int(np.where(pid == 'A15058075')[0])
# row = 344
rate = rating[row]
binary_seen = seen(row)
for k in range(len(prob)):
    if binary_seen[k] == 1:
        continue
    sum = 0
    for i in range(4):
        sum += rou_it(final_Z, final_R, i, row) * final_R[k][i]
    prob[k] = sum
index_mine = {}
for i in range(len(prob)):
    if prob[i] == 0:
        continue
    index_mine[i] = prob[i]

index_mine_sorted = sorted(index_mine.items(), key=lambda x: x[1], reverse=True)
movie_mine_sorted = []
for i in range(len(index_mine_sorted)):
    movie_mine_sorted.append(movie[index_mine_sorted[i][0]])
print(movie_mine_sorted)
