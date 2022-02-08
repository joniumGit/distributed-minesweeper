import random

import matplotlib.pyplot as plt
import numpy as np
from minesweeper.logic import Field, iter_2d
from alt_generate import Dummy

if __name__ == '__main__':

    plt.switch_backend('macosx')

    while True:
        fig, axs = plt.subplots(1, 2, sharex='all', sharey='all')
        ax1, ax2 = axs

        mines = random.randint(1000, int(100 ** 2 * 0.99))
        f1 = Field(100, 100, mines)
        f2 = Dummy(100, 100, mines)

        f1.generate()
        f2.generate()

        im1 = list(map(lambda _: list(map(lambda _: 0, range(0, 100))), range(0, 100)))
        im2 = list(map(lambda _: list(map(lambda _: 0, range(0, 100))), range(0, 100)))
        for x, y in iter_2d(100, 100):
            im1[x][y] = f1[x, y]
            im2[x][y] = f2[x, y]
        im1 = np.asarray(im1)
        im2 = np.asarray(im2)

        ax1.imshow(im1, cmap=plt.cm.binary)
        ax2.imshow(im2, cmap=plt.cm.binary)

        ax1.set_title('Shuffle')
        ax2.set_title('Rand 2D')

        plt.suptitle(f'Mine rate {mines / 100 ** 2 * 100:.2f}%')
        plt.show()
