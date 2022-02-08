import gc
import multiprocessing

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def gen_params():
    from math import ceil
    from itertools import chain
    for width in chain(
            # range(2, 100, 1),
            # range(70, 100, 1)
            range(50, 100, 5),
            # range(100, 650, 50)
    ):
        _max = ceil((width - 1) ** 2 / width ** 2 * 100)
        for params in ((width, width, float(f'0.{f:02d}'), b) for f in range(
                1,
                _max,
                2
        ) for b in (
                               True,
                               # False
                       )):
            yield params


def simu(params):
    import time
    from minesweeper.logic import Field
    from alt_generate import Dummy

    width, height, mines, shuffle = params

    gc.disable()

    s = time.time_ns()
    f = (Field if shuffle else Dummy)(width, height, int(width * height * mines))
    f.generate()
    e = time.time_ns()
    execution_time = (e - s) / 1E6
    gc.collect()

    for _ in range(0, 10):
        s = time.time_ns()
        f = (Field if shuffle else Dummy)(width, height, int(width * height * mines))
        f.generate()
        e = time.time_ns()
        execution_time = execution_time / 2 + (e - s) / 2E6
        gc.collect()

    mt = width * height / ((width - 1) * (height - 1))
    if (width % 10 == 0 and width < 100 or width % 100 == 0 and width < 1000 or width % 1000 == 0) and mines >= mt:
        print(f'Done with w={width},h={width},s={shuffle}')

    return *params, execution_time


def plot(data: np.ndarray, below: int):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    ax: Axes3D

    data_shuffle = data[np.logical_and(data[:, -2] == True, data[:, 1] < below)]
    data_rand_2d = data[np.logical_and(np.logical_not(data[:, -2] == True), data[:, 1] < below)]

    for _data, label, cm in zip(
            [data_shuffle, data_rand_2d],
            ['shuffle', 'rand_2d (bright)'],
            [plt.cm.coolwarm, plt.cm.bwr]
    ):
        if len(_data) == 0:
            continue
        surf = ax.plot_trisurf(
            _data[:, 0],
            _data[:, 2],
            _data[:, -1],
            # cmap=cm,
            linewidth=1,
            # shade=False,
            label=label,
            alpha=0.5,
            zorder=10
        )
        surf._facecolors2d = surf._facecolor3d
        surf._edgecolors2d = surf._edgecolor3d

    ax.set_xlabel('Width/Height (n)')
    ax.set_ylabel('Mines (%)')
    ax.set_zlabel('Execution Time (ms)')

    plt.legend()
    plt.show()


if __name__ == '__main__':
    import os

    plt.switch_backend('macosx')

    path = os.path.join(__file__.replace('/main.py', ''), 'cachefile.npy')
    print(path)
    if not os.path.exists(path):
        with multiprocessing.Pool() as p:
            data = np.asarray(p.map(simu, gen_params()))
        print('Saving...')
        np.save(path, data)
        print('Done')
        gc.enable()
    else:
        print('Loading...')
        data = np.load(path)
        print('Done')

    plot(data, 1000)
    plot(data, 100)
