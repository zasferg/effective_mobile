import random
from typing import Generator, List, Tuple


class Cell:

    def __init__(self, around_mines: int = 0, mine: bool = False) -> None:
        self.around_mines: int = around_mines
        self.mine: bool = mine
        self.__fl_open: bool = False
        self.__clicked: bool = False

    @classmethod
    def __check_for_bool(cls, value: bool) -> None:
        if not isinstance(value, bool):
            raise ValueError("Bad value.")
    
    @property
    def cell_status(self) -> bool:
        return self.__fl_open
    
    @cell_status.setter
    def cell_status(self, fl: bool) -> None:
        self.__check_for_bool(fl)
        self.__fl_open = fl

    @property
    def clicked(self) -> bool:
        return self.__clicked
    
    @clicked.setter
    def clicked(self, val: bool) -> None:
        self.__check_for_bool(val)
        self.__clicked = val



class GamePole:

    def __init__(self, N: int, M: int) -> None:

        self.field_dimension: int = N
        self.mines_count: int = M
        self.__field: List[List[Cell]] = [
            [Cell() for j in range(self.field_dimension)]
            for i in range(self.field_dimension)
        ]
        self.show_list: List[List[str]] = [
            ["." for j in range(self.field_dimension)]
            for i in range(self.field_dimension)
        ]

    def __set_mine_cell_coords(self) -> Generator[Tuple[int, int], None, None]:

        used_cells: List[Tuple[int, int]] = []

        while True:
            cell_i: int = random.randint(0, self.field_dimension - 1)
            cell_j: int = random.randint(0, self.field_dimension - 1)

            if (cell_i, cell_j) not in used_cells:
                used_cells.append((cell_i, cell_j))
                yield (cell_i, cell_j)

    def init_field(self) -> None:

        for _ in range(self.mines_count):
            cell_i, cell_j = next(self.__set_mine_cell_coords())
            self.__field[cell_i][cell_j].mine = True

        for index_raw in range(self.field_dimension):
            for index_coll in range(self.field_dimension):
                if not self.__field[index_raw][index_coll].mine:
                    mines_count_list: List[bool] = []
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if not (i == 0 and j == 0):
                                ni, nj = index_raw + i, index_coll + j
                                if (
                                    0 <= ni < self.field_dimension
                                    and 0 <= nj < self.field_dimension
                                ):
                                    mines_count_list.append(self.__field[ni][nj].mine)
                    self.__field[index_raw][index_coll].around_mines = sum(
                        mines_count_list
                    )

    def show_field(self) -> None:

        for index_raw, raw in enumerate(self.__field):
            for index_coll, item in enumerate(raw):
                if item.cell_status:
                    if item.clicked:
                        self.show_list[index_raw][index_coll] = "#"
                    elif item.mine:
                        self.show_list[index_raw][index_coll] = "*"
                    else:
                        self.show_list[index_raw][index_coll] = str(item.around_mines)
                else:
                    pass

        for row in self.show_list:
            print(row)

    def check_mine(self, raw: int, coll: int) -> bool:

        if not isinstance(raw, int) or not isinstance(coll, int):
            raise TypeError("Bad value type")

        if (
            raw < 0
            or raw > self.field_dimension
            or coll < 0
            or coll > self.field_dimension
        ):
            raise ValueError("Bad value")

        converted_raw: int = raw - 1
        converted_col: int = coll - 1

        cell: Cell = self.__field[converted_raw][converted_col]

        if cell.cell_status:
            print("You have already checked this cell!")
            return True

        elif cell.mine:
            print("--------Boom!!-----------")
            return False
        else:
            cell.cell_status = True
            cell.clicked = True

            for i in range(-1, 2):
                for j in range(-1, 2):
                    if not (i == 0 and j == 0):
                        ni, nj = converted_raw + i, converted_col + j
                        if (
                            0 <= ni < self.field_dimension
                            and 0 <= nj < self.field_dimension
                        ):
                            self.__field[ni][nj].cell_status = True

            print("Good, check other cell!")
            return True

    def init_game_loop(self) -> None:

        while True:
            if all(item.cell_status for rows in self.__field for item in rows):
                print("You win!")
                break

            raw: int = int(input("Please enter the row number: "))
            coll: int = int(input("Please enter the column number: "))

            if not self.check_mine(raw, coll):
                break

            self.show_field()


def game_loop() -> None:
    dimension: int = int(input("Please enter field dimension: "))
    mines_count: int = int(input("Please enter number of mines: "))

    pole_game: GamePole = GamePole(dimension, mines_count)
    pole_game.init_field()
    pole_game.init_game_loop()


game_loop()
