# Import the pygame module
import random
from typing import List
import pygame
from tetrominos import *
from pygame.locals import (
    QUIT,
)

pygame.init()


class Game:
    DEFAULT_TETRO_SPAWN = ((GAMEZONE_WIDTH - 100) // 2, 0)

    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.fill((255, 255, 255))
        self.gamezone = pygame.Surface((GAMEZONE_WIDTH, GAMEZONE_HEIGHT))
        self.gamezone.fill(BACKGROUND_COLOR)

        self.border_boxes = {
            "l": Rect(0, 0, 1, GAMEZONE_HEIGHT),
            "r": Rect(GAMEZONE_WIDTH - 1, 0, 1, GAMEZONE_HEIGHT),
            "b": Rect(0, GAMEZONE_HEIGHT - 1, GAMEZONE_WIDTH, 10),
        }

        pygame.draw.rect(self.gamezone, (13, 124, 13), self.border_boxes.get("b"))

    def get_next_tetro(self) ->Tetromino:
        i = random.randint(0, TetrominoFactory.NB_TETROMINOS)
        return TetrominoFactory.get_tetrominos()[2]
        # print(f"Current tetro {current_tetro.rect}")

    def drawGrid(self):
        blockSize = TETRO_SIZE  # Set the size of the grid block
        for x in range(0, GAMEZONE_WIDTH, blockSize):
            for y in range(0, GAMEZONE_HEIGHT, blockSize):
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(self.screen, GRID_LINE_COLOR, rect, 1)

    def play(self):
        played_tetros: List[Tetromino] = []

        running = True
        is_tetro_played = False
        clock = pygame.time.Clock()

        self.get_next_tetro()
        current_tetro = self.get_next_tetro()
        # Main loop
        while running:
            # for loop through the event queue
            self.drawGrid()
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            current_tetro.draw(self.screen)

            pressed_keys = pygame.key.get_pressed()
            move_tetro_lr = True
            for tetro in played_tetros:
                if current_tetro.check_collision(tetro):
                    is_tetro_played = True
                    break

            for rect in current_tetro.rects:
                if (
                    rect.colliderect(self.border_boxes.get("l"))
                    and pressed_keys[K_LEFT]
                ):
                    move_tetro_lr = False
                    break

                if (
                    rect.colliderect(self.border_boxes.get("r"))
                    and pressed_keys[K_RIGHT]
                ):
                    move_tetro_lr = False
                    break
                if rect.colliderect(self.border_boxes.get("b")):
                    is_tetro_played = True
                    break

            if is_tetro_played:
                played_tetros.append(current_tetro)
                current_tetro = self.get_next_tetro()
                is_tetro_played = False
            else:
                current_tetro.move(
                    pressed_keys,
                    move_tetro_lr,
                    played_tetros,
                    self.border_boxes,
                )

            for tetro in played_tetros:
                tetro.draw(self.screen)

            pygame.display.flip()

            self.screen.blit(self.gamezone, self.gamezone.get_rect())
            # self.screen.blit(bottom_box.surf, (0, GAMEZONE_HEIGHT - 100))
            clock.tick(GAME_SPEED // 5)


if __name__ == "__main__":
    game = Game()
    game.play()
