#!/usr/bin/env python3
"""Play Snake in the terminal using curses.

Controls:
- Arrow keys or WASD to move
- Q to quit
"""

from __future__ import annotations

import curses
import random
import time
from dataclasses import dataclass

TICK_SECONDS = 0.10
MIN_WIDTH = 20
MIN_HEIGHT = 10


@dataclass(frozen=True)
class Point:
    y: int
    x: int


DIRECTIONS = {
    curses.KEY_UP: Point(-1, 0),
    curses.KEY_DOWN: Point(1, 0),
    curses.KEY_LEFT: Point(0, -1),
    curses.KEY_RIGHT: Point(0, 1),
    ord("w"): Point(-1, 0),
    ord("s"): Point(1, 0),
    ord("a"): Point(0, -1),
    ord("d"): Point(0, 1),
}


class SnakeGame:
    def __init__(self, screen: curses.window) -> None:
        self.screen = screen
        self.height, self.width = screen.getmaxyx()
        self.play_height = self.height - 2
        self.play_width = self.width - 2
        self.snake: list[Point] = []
        self.direction = Point(0, 1)
        self.food = Point(0, 0)
        self.score = 0

    def validate_size(self) -> None:
        if self.width < MIN_WIDTH or self.height < MIN_HEIGHT:
            raise ValueError(
                f"Terminal too small ({self.width}x{self.height}). "
                f"Need at least {MIN_WIDTH}x{MIN_HEIGHT}."
            )

    def reset(self) -> None:
        mid_y = self.play_height // 2 + 1
        mid_x = self.play_width // 2 + 1
        self.snake = [
            Point(mid_y, mid_x + 1),
            Point(mid_y, mid_x),
            Point(mid_y, mid_x - 1),
        ]
        self.direction = Point(0, 1)
        self.score = 0
        self.food = self._spawn_food()

    def _spawn_food(self) -> Point:
        occupied = set(self.snake)
        available = [
            Point(y, x)
            for y in range(1, self.height - 1)
            for x in range(1, self.width - 1)
            if Point(y, x) not in occupied
        ]
        if not available:
            return Point(-1, -1)
        return random.choice(available)

    def _draw_border(self) -> None:
        self.screen.border()

    def _draw_status(self) -> None:
        status = f" Score: {self.score} | Arrow keys / WASD | Q quit "
        self.screen.addnstr(0, 2, status, self.width - 4)

    def _draw_food(self) -> None:
        if self.food.y >= 1:
            self.screen.addch(self.food.y, self.food.x, "*")

    def _draw_snake(self) -> None:
        for i, part in enumerate(self.snake):
            char = "@" if i == 0 else "#"
            self.screen.addch(part.y, part.x, char)

    def _next_head(self) -> Point:
        head = self.snake[0]
        return Point(head.y + self.direction.y, head.x + self.direction.x)

    def _is_opposite(self, new_dir: Point) -> bool:
        return (
            self.direction.y + new_dir.y == 0
            and self.direction.x + new_dir.x == 0
        )

    def handle_input(self, key: int) -> bool:
        if key in (ord("q"), ord("Q")):
            return False

        new_dir = DIRECTIONS.get(key)
        if new_dir and not self._is_opposite(new_dir):
            self.direction = new_dir

        return True

    def step(self) -> bool:
        next_head = self._next_head()

        hit_wall = (
            next_head.y <= 0
            or next_head.y >= self.height - 1
            or next_head.x <= 0
            or next_head.x >= self.width - 1
        )
        hit_self = next_head in self.snake

        if hit_wall or hit_self:
            return False

        self.snake.insert(0, next_head)

        if next_head == self.food:
            self.score += 1
            self.food = self._spawn_food()
        else:
            self.snake.pop()

        return True

    def draw(self) -> None:
        self.screen.erase()
        self._draw_border()
        self._draw_status()
        self._draw_food()
        self._draw_snake()
        self.screen.refresh()


def run(screen: curses.window) -> None:
    curses.curs_set(0)
    screen.nodelay(True)
    screen.timeout(0)
    screen.keypad(True)

    game = SnakeGame(screen)

    try:
        game.validate_size()
    except ValueError as error:
        screen.clear()
        screen.addstr(1, 1, str(error))
        screen.addstr(3, 1, "Resize your terminal and try again.")
        screen.addstr(5, 1, "Press any key to exit.")
        screen.nodelay(False)
        screen.getch()
        return

    game.reset()
    last_tick = time.monotonic()

    while True:
        key = screen.getch()
        if key != -1 and not game.handle_input(key):
            return

        now = time.monotonic()
        if now - last_tick >= TICK_SECONDS:
            last_tick = now
            if not game.step():
                break

        game.draw()
        time.sleep(0.005)

    screen.nodelay(False)
    game.draw()
    screen.addstr(game.height // 2, max(2, game.width // 2 - 5), "GAME OVER")
    screen.addstr(game.height // 2 + 1, max(2, game.width // 2 - 11), f"Final score: {game.score}")
    screen.addstr(game.height // 2 + 3, max(2, game.width // 2 - 12), "Press any key to exit")
    screen.refresh()
    screen.getch()


if __name__ == "__main__":
    curses.wrapper(run)
