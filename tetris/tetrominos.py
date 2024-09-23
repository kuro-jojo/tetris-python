# Import the pygame module
import os
from typing import List
from pygame import Surface, Rect
from config import *
import pygame
from pygame.image import load
from pygame.sprite import Sprite
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
)


class TetrominoFactory:
    TYPES = ("I", "J", "L", "O", "S", "T", "Z")
    NB_TETROMINOS = 6

    @staticmethod
    def get_tetromino(
        shape: str, orientation: int, offset: tuple = (0, 0, 0, 0)
    ) -> List[Rect]:
        if shape not in TetrominoFactory.TYPES:
            raise ValueError("Unknown tetromino type")

        tetro = TETROMINO_SHAPES.get(shape)[orientation]
        tetro_rects: List[Rect] = []

        for row in range(0, len(tetro)):
            for col in range(0, len(tetro[row])):
                if tetro[row][col]:
                    rect = Rect(
                        col * TETRO_SIZE + offset[0],
                        row * TETRO_SIZE + offset[1],
                        TETRO_SIZE + offset[2],
                        TETRO_SIZE + offset[3],
                    )
                    tetro_rects.append(rect)

        return tetro_rects

    def get_tetrominos() -> List:
        return [
            ITetromino(),
            STetromino(),
            ZTetromino(),
            JTetromino(),
            LTetromino(),
            TTetromino(),
            OTetromino(),
        ]


class Tetromino(Sprite):
    def __init__(
        self,
        type: str,
        orientation: int = 0,
        offset: tuple = (0, 0, 0, 0),
        rotation_matrix: List = [],
    ):
        super(Tetromino, self).__init__()
        self.type = type
        self.orientation = orientation
        self.offset = offset
        self.rects = TetrominoFactory.get_tetromino(type, orientation, offset)
        self.rotation_matrix = rotation_matrix

    def move(
        self,
        pressed_keys: int,
        move_lr: bool = True,
        others: List["Tetromino"] = [],
        gamezone_hitboxes: dict[str,Rect] = None,
    ):
        if move_lr:
            if pressed_keys[K_LEFT]:
                self.__move(-GAME_SPEED, 0)
            elif pressed_keys[K_RIGHT]:
                self.__move(GAME_SPEED, 0)

        if pressed_keys[K_UP]:
            self.rotate(others, gamezone_hitboxes)

        if pressed_keys[K_DOWN]:
            skip = False
            # tmp_tetro = Tetromino(self.type)
            # if bottom_area:
            #     tmp_tetro.rects = [bottom_area]
            #     print(tmp_tetro.rects, others)
            #     others.append(tmp_tetro)
            # tmp_tetro.rects = [r.move(0, GAME_SPEED) for r in self.rects]
            # for o in others:
            #     if tmp_tetro.collide_other(o):
            #         print(tmp_tetro.rects)
            #         skip = True
            if not skip:
                self.__move(0, DOWN_SPEED)

        elif not pressed_keys[K_SPACE]:
            self.__move(0, GAME_SPEED)

    def __move(self, x: int, y: int):
        for rect in self.rects:
            rect.move_ip(x, y)

    def adjustOrientation(
        self,
        prev_tetro: "Tetromino",
        other_tetros: List["Tetromino"],
        gamezone_hitboxes: dict[str,Rect],
        inversed: bool = False,
    ):
        assert len(self.rotation_matrix) == 4, "Matrix of rotation (2x4) is needed"
        tmp_rects = list()
        prev_rects = prev_tetro.rects
        for i in range(len(self.rects)):
            vec = self.rotation_matrix[i]
            rect = prev_rects[i]
            if inversed:
                vec = [-v for v in vec]
            tmp_rects.append(
                Rect(
                    rect.left + vec[0] * 25,
                    rect.top + vec[1] * 25,
                    rect.width,
                    rect.height,
                )
            )
        rotated_tetro = Tetromino(self.type, self.orientation, self.offset)
        rotated_tetro.rects = tmp_rects
        if not rotated_tetro.check_collisions(
            other_tetros
        ) :
            prev_tetro.rects = rotated_tetro.rects

    def draw(self, screen: Surface):
        for rect in self.rects:
            pygame.draw.rect(screen, TETROMINO_COLORS[self.type], rect)

    def check_collisions(self, others: List["Tetromino"]) -> bool:
        for o in others:
            if self.check_collision(o):
                return True
        return False

    def check_collision(self, other: "Tetromino") -> bool:
        for r in self.rects:
            print("T", r.left)
            
            for o_r in other.rects:
                if r.bottom >= o_r.top and (
                    (r.left < o_r.right and r.left > o_r.left)
                    or (r.right < o_r.right and r.right > o_r.left)
                    or (r.left == o_r.left and r.right == o_r.right)
                ):
                    return True

        return False

    def check_collision_rect(self, rects: dict[str,Rect]) -> bool:
        for rect in self.rects:
            l = rects.get("l")
            r = rects.get("r")
            b = rects.get("b")
            if rect.left < l.right:
                print("Tl", rect.left, l.right)
                return True
            if rect.right > r.left:
                print("Tr")
                return True
            if rect.bottom < b.top:
                print("Tb")
                return True
        return False

    def rotate(self, other_tetros: List["Tetromino"], gamezone_hitboxes: dict[str,Rect]):
        pass


class OneVarationTetromino(Tetromino):
    def __init__(
        self,
        type: str,
        orientation: int = 0,
        offset: tuple = (0, 0, 0, 0),
        rotation_matrix: List = [],
    ):
        super().__init__(type, orientation, offset, rotation_matrix)
        self.orientation = orientation

    def rotate(self, other_tetros: List["Tetromino"], gamezone_hitboxes: dict[str,Rect]):
        if self.orientation == 0:  # Horizontal
            tmp_tetro = OneVarationTetromino(
                self.type, 1, self.offset, self.rotation_matrix
            )
            tmp_tetro.adjustOrientation(self, other_tetros, gamezone_hitboxes)
            self.orientation = 1
        elif self.orientation == 1:  # Vertical
            tmp_tetro = OneVarationTetromino(
                self.type, 0, self.offset, self.rotation_matrix
            )
            tmp_tetro.adjustOrientation(self, other_tetros, gamezone_hitboxes, True)
            self.orientation = 0


class TwoVarationTetromino(Tetromino):
    def __init__(self, type: str):
        super().__init__(type)
        self.state = 0

    def rotate(self, other_tetros: List["Tetromino"] = []):
        orientation = (self.state + 1) % 4
        self.rects = TetrominoFactory.get_tetromino(self.type, orientation)
        self.state = orientation


class ITetromino(OneVarationTetromino):
    def __init__(self):
        super().__init__(
            "I",
            offset=(TETRO_SIZE * 3, 0, 0, 0),
            rotation_matrix=[[2, -1], [1, 0], [0, 1], [-1, -2]],
        )


class STetromino(OneVarationTetromino):
    def __init__(self):
        super().__init__("S", rotation_matrix=[[1, 1], [0, 2], [1, -1], [0, 0]])


class ZTetromino(OneVarationTetromino):
    def __init__(self):
        super().__init__("Z", rotation_matrix=[[2, 0], [1, 1]] * 2)


class LTetromino(TwoVarationTetromino):
    def __init__(self):
        super().__init__("L")


class JTetromino(TwoVarationTetromino):
    def __init__(self):
        super().__init__("J")


class TTetromino(TwoVarationTetromino):
    def __init__(self):
        super().__init__("T")


class OTetromino(Tetromino):
    def __init__(self):
        super().__init__("O", offset=(TETRO_SIZE * 4, 0, 0, 0))
