import numpy as np
import pandas as pd


def main():
    pass


# names = lambda int: str(chr(65+int))
names = 'ABCDEFGHIJKLMNOPQRS'


def cluster(k: int, coords: np.array):
    x = coords[:, 0]
    y = coords[:, 1]
    locs = list(names[:k])

    df = pd.DataFrame(columns=locs, index=coords)
    k_locs = dict()

    for i in range(k):
        ran_x = np.random.randint(x.min(), x.max())
        ran_y = np.random.randint(y.min(), y.max())
        print('x', ran_x)
        print('y', ran_y)
        k_locs[names[i]] = np.array((ran_x, ran_y))

    for loc in locs:
        distances = distances_from_point(k_locs[loc], coords)
        df.loc[:, loc] = distances

    return df


def distances_from_point(point: np.array, points: np.array) -> np.array:
    """gives array of length points containing the Euclidean distance of Cs to point B"""
    return np.linalg.norm(points - point, axis=1)
    # https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy


if __name__ == '__main__':
    # main()
    K = 2
    coords = np.array([(1, 1), (2, 2), (10, 15), (8, -12), (14, 100)])
    df = cluster(K, coords)

# where c is a numpy array of coorsd & b is a numpy coord of interest
# C = np.array([(1,1),(4,4)])
# B = np.array((2,2))
# np.linalg.norm(C-B, axis=1)
# gives array of length C where each element is the elucidian distance of item in C to point B
