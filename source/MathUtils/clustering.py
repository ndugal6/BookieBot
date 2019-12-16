import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def main():
    pass


# names = lambda int: str(chr(65+int))
names = 'ABCDEFGHIJKLMNOPQRS'


# locs = list(names[:k])

def cluster(k: int, coords: np.array, k_locs=None, df=None):
    x = coords[:, 0]
    y = coords[:, 1]
    locs = list(names[:k])

    if df is None:
        cols = ['COORDS'] + locs
        df = pd.DataFrame(columns=cols)

        string_coords = list(map(stringify_coords, list(coords)))
        df['COORDS'] = string_coords
        df['MEMBERSHIP'] = 'N/A'
        df['X'] = x
        df['Y'] = y

    if k_locs is None:
        k_locs = dict()
        for loc in locs:
            ran_x = np.random.randint(x.min(), x.max())
            ran_y = np.random.randint(y.min(), y.max())
            print('x', ran_x)
            print('y', ran_y)
            k_locs[loc] = np.array((ran_x, ran_y))

    for cluster_id, cluster_position in k_locs.items():
        distances = distances_from_point(cluster_position, coords)
        df.loc[:, cluster_id] = distances

    mins = min_distances(df, locs)
    for row, min in enumerate(mins):
        col = get_column_given_value(min, df)
        df.at[row, 'MEMBERSHIP'] = col

    return (df, k_locs)


def distances_from_point(point: np.array, points: np.array) -> np.array:
    """gives array of length points containing the Euclidean distance of Cs to point B"""
    return np.linalg.norm(points - point, axis=1)
    # https://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy


def get_column_given_value(value, df):
    return df.columns[df.isin([value]).any()][0]


def min_distances(df, locs) -> pd.Series:
    return df.loc[:, locs].T.min()


def stringify_coords(a):
    seperator = '_'
    a_corrected = list(map(str, a))
    return seperator.join(list(a_corrected))


def k_mean_clustering():
    k = 3
    threshold = 0.5
    convergance_limit = 10
    coords = np.array([(1, 1), (2, 2), (10, 15), (8, -12), (14, 100)])
    df, klocs = cluster(k, coords)

    count = 1
    while True:
        cluster_too_far = False
        for cluster_id, cluster_position in klocs.items():
            new_x = df[df.MEMBERSHIP == cluster_id]['X'].mean()
            new_y = df[df.MEMBERSHIP == cluster_id]['Y'].mean()
            new_coords = np.array((new_x, new_y))
            if not cluster_too_far:
                distance = np.linalg.norm(new_coords - cluster_position)
                cluster_too_far = distance > threshold
            klocs[cluster_id] = new_coords

        if not cluster_too_far:
            print('converged by interation', count)
            break
        count += 1
        if count > convergance_limit:
            print("unable to converge")
            break
        df, klocs = cluster(k, coords, k_locs=klocs, df=df)


if __name__ == '__main__':
    # main()
    k = 3
    threshold = 0.05
    convergance_limit = 10
    coords = np.array([(1, 1), (2, 2), (10, 15), (8, -12), (-5,-10), (-15,15), (10,-15),(-10,15), (-1,-1), (20,20), (-8,-12)])
    df, klocs = cluster(k, coords)
    index = df.index

    count = 1
    while True:
        cluster_too_far = False
        for cluster_id, cluster_position in klocs.items():
            new_x = df[df.MEMBERSHIP == cluster_id]['X'].mean()
            new_y = df[df.MEMBERSHIP == cluster_id]['Y'].mean()
            new_coords = np.array((new_x, new_y))
            if not cluster_too_far:
                distance = np.linalg.norm(new_coords - cluster_position)
                cluster_too_far = distance > threshold
            klocs[cluster_id] = new_coords

        df, klocs = cluster(k, coords, k_locs=klocs, df=df)
        if not cluster_too_far:
            print('converged by interation', count)
            break
        count += 1
        if count > convergance_limit:
            print("unable to converge")
            break


    plt.figure()

    group_A = df[df.MEMBERSHIP == 'A']
    group_B = df[df.MEMBERSHIP == 'B']
    group_C = df[df.MEMBERSHIP == 'C']
    # plt.xm
    plt.scatter(group_A['X'], group_A['Y'], s=10, marker='.', c='r')
    plt.scatter(group_B['X'], group_B['Y'], s=10, marker='.', c='b')

    plt.scatter(klocs['A'][0], klocs['A'][1], s=20, marker='x', c='r')
    plt.scatter(klocs['B'][0], klocs['B'][0], s=20, marker='x', c='b')

    plt.scatter(group_C['X'], group_C['Y'], s=10, marker='o', c='k')
    plt.scatter(klocs['C'][0], klocs['C'][0], s=20, marker='x', c='k')
    print(klocs)
    plt.show()

# where c is a numpy array of coorsd & b is a numpy coord of interest
# C = np.array([(1,1),(4,4)])
# B = np.array((2,2))
# np.linalg.norm(C-B, axis=1)
# gives array of length C where each element is the elucidian distance of item in C to point B

# df[df == df.loc[0,:].max()] outputs NAN except for value
# df1.loc[lambda df: df.A > 18, :] will filter & not give NA
