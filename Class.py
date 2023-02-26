from Exception_ import *
from random import randint

class Game:
    def __init__(self,size=6):
        self.size=size
        person = self.random_board()
        pc = self.random_board()
        pc.hid=True

        self.ai=AI(pc,person)
        self.us = User(person, pc)


    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Pixel(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            if num % 2 == 0:
                print("-" * 20)
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("-" * 20)
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1
    def game(self):
        self.hello()
        self.loop()

    @staticmethod
    def hello():
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

class Pixel:
    def __init__(self,x,y):
        self.x=x
        self.y=y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f"({self.x}, {self.y})"

class Ship():
    def __init__(self,pix,l,pos):
        self.pixel=pix
        self.length=l
        self.position=pos
        self.healf=l
    @property
    def pixelship(self):
        ship_pixels=[]
        for _ in range(self.length):
            pos_x=self.pixel.x
            pos_y=self.pixel.y
            if (self.position==0):
                pos_x+=_
            elif (self.position==1):
                pos_y+=_
            ship_pixels.append(Pixel(pos_x,pos_y))
        return ship_pixels

    def shoot(self, pix):
        return pix in self.pixelship
class Board():
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid
        self.count = 0
        self.field = [["O"] * size for _ in range(size)]
        self.busy = []
        self.ships = []

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("■", "O")
        return res

    def out(self, pix):
        return not ((0 <= pix.x < self.size) and (0 <= pix.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for p in ship.pixelship:
            for px, py in near:
                cur = Pixel(p.x + px, p.y + py)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship(self, ship):

        for p in ship.pixelship:
            if self.out(p) or p in self.busy:
                raise BoardWrongShipException()
        for p in ship.pixelship:
            self.field[p.x][p.y] = "■"
            self.busy.append(p)

        self.ships.append(ship)
        self.contour(ship)

    def shot(self, p):
        if self.out(p):
            raise BoardOutException()

        if p in self.busy:
            raise BoardUsedException()

        self.busy.append(p)

        for ship in self.ships:
            if p in ship.pixelship:
                ship.healf -= 1
                self.field[p.x][p.y] = "X"
                if ship.healf == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль ранен!")
                    return True

        self.field[p.x][p.y] = "."
        print("Мимо!")
        return False

    def begin(self):
        self.busy = []

class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        p = Pixel(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {p.x + 1} {p.y + 1}")
        return p

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Pixel(x - 1, y - 1)



