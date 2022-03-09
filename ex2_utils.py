from random import randint

IPADDR = "127.0.0.1"  # IP address of the server (listening on this address)
PORT = 8820  # Port of the server (listening on this port)

MAX_MSG_SIZE = 1024  # Maximum length of message of the socket

MAPS = {'1': "icehockey.bin", # list of map addresses using number as a key
        '2': "pacman.bin",
        '3': "randomwalls.bin"
        }


def get_arena(arena_type):
    list_of_squares = [] # 2D array of squares
    with open(MAPS[arena_type], "br") as f:
        one_line = [] # a list of squares which will constitute one line
        line_number = 1
        line_length = int.from_bytes(f.read(1), "big") # line length using the first char
        line = f.read(line_length - 1)
        one_line.append(square(1, 1, True)) # adds the first square, a wall, in (1, 1)
        for i in range(len(line)):
            is_wall = False
            if line[i] != 0:
                is_wall = True
            square1 = square(i + 2, line_number, is_wall) # makes a square in the coords. 0 for a wall, 1 for a passage
            one_line.append(square1) # adds square to the list
        list_of_squares.append(one_line) # adds list to the 2D list
        line_number = 2
        end = False
        try: # adds the rest of the lines
            while not end:
                one_line = []
                first = f.read(1)
                if first != 0:
                    is_wall_first = True
                line = f.read(line_length - 1)
                for i in range(line_length - 1):
                    is_wall = False
                    if line[i] != 0:
                        is_wall = True
                    square1 = square(line_number, i + 2, is_wall)
                    one_line.append(square1)
                one_line.append(square(line_number, line_length, is_wall_first))
                list_of_squares.append(one_line)
                line_number += 1
        except:
            return list_of_squares


def print_empty_arena(list_of_squares):  # used that while coding
    x = [""]
    for i in list_of_squares:
        for j in i:
            x.append(j.get_type())
        x.append("\n")
    print(" ".join(x))


class square: # everyone square will be presented by an object
    def __init__(self, x, y, is_wall):
        self.__x = x # coord x
        self.__y = y # coord y
        self.__is_wall = is_wall
        self.__content = None # contains the thief (or not)
        self.__is_treasure = False
        self.__is_cop = False

    def __str__(self): # self-explanatory
        if self.__content == "thief":
            return "X"
        elif self.__is_cop:
            return "C"
        elif self.__is_treasure:
            return "T"
        elif self.__is_wall:
            return "*"
        return " "

    def set_treasure(self): # self-explanatory
        self.__is_treasure = True

    def set_cop(self): # self-explanatory
        self.__is_cop = True

    def remove_cop(self): # self-explanatory
        self.__is_cop = False

    def is_wall(self): # self-explanatory
        return self.__is_wall

    def is_treasure(self): # self-explanatory
        if self.__is_treasure:
            return True

    def is_cop(self): # self-explanatory
        if self.__is_cop:
            return True

    def get_type(self): # self-explanatory
        if self.__content == "thief":
            return "X"
        elif self.__is_cop:
            return "C"
        elif self.__is_treasure:
            return "T"
        elif self.__is_wall:
            return "*"
        return " "

    def get_location(self): # self-explanatory
        return (self.__x, self.__y)

    def set_content(self, type): # self-explanatory
        self.__content = type


class Arena:
    def __init__(self, list_of_squares): # initialises arena using list of squares, dimensions and random squares for Thief, Treasure & Cop
        self.__squares = list_of_squares
        self.__dimensions = self.__squares[-1][-1].get_location()
        self.__cop = self.get_empty_coords()
        self.__squares[self.__cop[0] - 1][self.__cop[1] - 1].set_cop()
        self.__thief = self.get_empty_coords()
        self.__squares[self.__thief[0] - 1][self.__thief[1] - 1].set_content("thief")
        self.__treasure = self.get_empty_coords()
        self.__squares[self.__treasure[0] - 1][self.__treasure[1] - 1].set_treasure()

    def __str__(self): # self-explanatory
        x = [""]
        for i in self.__squares:
            for j in i:
                x.append(j.get_type())
            x.append("\n")
        return " ".join(x)

    def get_empty_coords(self): # gets random coords, checks in the list if it's a wall
        coords = (randint(1, self.__dimensions[0]), randint(1, self.__dimensions[1]))
        while self.__squares[coords[0] - 1][coords[1] - 1].is_wall():
            coords = (randint(1, self.__dimensions[0]), randint(1, self.__dimensions[1]))
        return coords

    def game_over(self): # whether the thief is on treasure, cop or both
        if self.__squares[self.__thief[0] - 1][self.__thief[1] - 1].is_treasure() or self.__squares[self.__thief[0] - 1][self.__thief[1] - 1].is_cop():
            return True
        return False

    def check_win(self): # self-explanatory
        if self.__squares[self.__thief[0] - 1][self.__thief[1] - 1].is_treasure():
            return True
        return False

    def check_lose(self): # self-explanatory
        if self.__squares[self.__thief[0] - 1][self.__thief[1] - 1].is_cop():
            return True
        return False

    def can_be_moved(self, move): # checks every case of thief movement, if possible to move returns 'True'
        if move == "up":
            if self.__thief[0] > 2:
                if not self.__squares[self.__thief[0] - 2][self.__thief[1] - 1].is_wall():
                    return True
        elif move == "down":
            if self.__thief[0] < self.__dimensions[0]:
                if not self.__squares[self.__thief[0]][self.__thief[1] - 1].is_wall():
                    return True
        elif move == "right":
            if self.__thief[1] < self.__dimensions[1]:
                if not self.__squares[self.__thief[0] - 1][self.__thief[1]].is_wall():
                    return True
        elif move == "left":
            if self.__thief[1] > 2:
                if not self.__squares[self.__thief[0] - 1][self.__thief[1] - 2].is_wall():
                    return True
        return False

    def move_thief(self, move): # moves thief by changing the square containing it accordingly and updates self__thief
        self.__squares[self.__thief[0] - 1][self.__thief[1] - 1].set_content(None)
        if move == "up":
            self.__squares[self.__thief[0] - 2][self.__thief[1] - 1].set_content("thief")
            self.__thief = (self.__thief[0] - 1, self.__thief[1])
        elif move == "down":
            self.__squares[self.__thief[0]][self.__thief[1] - 1].set_content("thief")
            self.__thief = (self.__thief[0] + 1, self.__thief[1])
        elif move == "left":
            self.__squares[self.__thief[0] - 1][self.__thief[1] - 2].set_content("thief")
            self.__thief = (self.__thief[0], self.__thief[1] - 1)
        else:
            self.__squares[self.__thief[0] - 1][self.__thief[1]].set_content("thief")
            self.__thief = (self.__thief[0], self.__thief[1] + 1)

    def move_cop(self): # moves the cop randomly to one of nine spots. if square is a wall, does nothing
        x = randint(-1, 1)
        y = randint(-1, 1)
        if not self.__squares[self.__cop[0] - 1 + x][self.__cop[1] - 1 + y].is_wall():
            self.__squares[self.__cop[0] - 1][self.__cop[1] - 1].remove_cop()
            self.__squares[self.__cop[0] - 1 + x][self.__cop[1] - 1 + y].set_cop()
            self.__cop = (self.__cop[0] + x, self.__cop[1] + y)

    def closeness(self): # for the status request, checks immediate closeness of the thief to the rest
        near_treasure = False
        near_cop = False
        if abs(self.__thief[0] - self.__treasure[0]) <= 1 and abs(self.__thief[1] - self.__treasure[1]) <= 1:
            near_treasure = True
        if abs(self.__thief[0] - self.__cop[0]) <= 1 and abs(self.__thief[1] - self.__cop[1]) <= 1:
            near_cop = True
        return near_treasure, near_cop
    