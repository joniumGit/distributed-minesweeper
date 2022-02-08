from minesweeper.logic import Field, MINE, n8, n8_safer, check_n8_safe, iter_edges


def rand_2d(rand, width: int, height: int):
    """
    Infinite stream of coordinates on a 2D plane from the random source provided.

    Assumes indexing [(0, width - 1), (0, height - 1)].

    :param rand:   Random source with method <i>randint(min, max)</i> with [min, max].
    :param width:  Width, first dimension
    :param height: Height, second dimension
    """
    width -= 1
    height -= 1
    while True:
        yield rand.randint(0, width), rand.randint(0, height)


# noinspection DuplicatedCode
class Dummy(Field):

    def generate(self) -> None:
        """
        Allocate space for the field and generate mines
        """
        from random import Random

        width = self.width
        height = self.height
        size = width * height
        mines = self.mines
        inverse = mines / size > 0.72  # Inverse is IF NOT -> IF -> ADD and normal is IF -> ADD
        rand = Random(self._seed)

        from itertools import takewhile
        self._data = bytearray(width * height)
        count = 0

        if not inverse:
            for x, y in takewhile(lambda _: count < mines, rand_2d(rand, width, height)):
                if self[x, y] & MINE:
                    continue
                self[x, y] |= MINE
                if check_n8_safe(x, y, width, height):
                    for dx, dy in n8(x, y):
                        self[dx, dy] += 1
                else:
                    for dx, dy in n8_safer(x, y, width, height):
                        self[dx, dy] += 1
                count += 1
        else:
            for x, y in takewhile(lambda _: count < mines, rand_2d(rand, width, height)):
                if self[x, y] & MINE:
                    continue
                self[x, y] |= MINE
                count += 1

        if inverse:
            for x in range(1, width - 1):
                for y in range(1, height - 1):
                    if not (self[x, y] & MINE):
                        for dx, dy in n8(x, y):
                            if self[dx, dy] & MINE:
                                self[x, y] += 1
            for x, y in iter_edges(width, height):
                    if not (self[x, y] & MINE):
                        for dx, dy in n8_safer(x, y, width, height):
                            if self[dx, dy] & MINE:
                                self[x, y] += 1
