import curses
from time import sleep
from life.classes import Grid, Pattern


type point = tuple[int, int]


class CursesView:
    def __init__(
            self,
            pattern: Pattern,
            generations=10,
            frame_rate=7,
            top_left=(0, 0),
            bottom_right=(20, 20)
    ) -> None:
        self.title = pattern.name
        self.pattern = pattern.cells
        self.generations = generations
        self.frame_delay = 1 / frame_rate
        self.top_left = top_left
        self.bottom_right = bottom_right
    
    def show(self) -> None:
        curses.wrapper(self._draw)
    
    def _draw(self, screen: "CursesWindow") -> None:
        curses.curs_set(0)
        screen.clear()

        grid = Grid(self.pattern)
        try:
            screen.addstr(" " + self.title + "\n")
            screen.addstr(1, 0, grid.window(self.top_left, self.bottom_right))
        except curses.error:
            raise ValueError
        for _ in range(self.generations):
            grid.evolve()
            sleep(self.frame_delay)
            screen.addstr(1, 0, grid.window(self.top_left, self.bottom_right))
            screen.refresh()
            