from termcolor import colored

p1_color = "red"
p2_color = "blue"
choice_color = "yellow"
board_size = 8


class Soldier:

    def __init__(self, color, row, col, num):
        self.color = color
        self.row = row
        self.col = col
        self.num = num

    def check_move(self, board):
        checked_options = []
        if self.color == p1_color:
            options = [(self.row - 1, self.col - 1), (self.row - 1, self.col + 1)]
            for n, option in enumerate(options):
                if option[1] < 0 or option[1] > board_size - 1:
                    continue
                else:
                    if board[option[0]][option[1]] != 0:
                        if board[option[0]][option[1]].color == self.color:
                            continue
                        else:
                            if self.row - 2 < 0:
                                continue
                            else:
                                if n == 0:
                                    if self.col - 2 < 0:
                                        continue
                                    else:
                                        if board[option[0] - 1][option[1] - 1] != 0:
                                            continue
                                        else:
                                            checked_options.append([(option[0] - 1, option[1] - 1),
                                                                    board[option[0]][option[1]]])
                                else:
                                    if self.col + 2 > board_size - 1:
                                        continue
                                    else:
                                        if board[option[0] - 1][option[1] + 1] != 0:
                                            continue
                                        else:
                                            checked_options.append([(option[0] - 1, option[1] + 1),
                                                                    board[option[0]][option[1]]])
                    else:
                        checked_options.append([option, 0])
        else:
            options = [(self.row + 1, self.col - 1), (self.row + 1, self.col + 1)]
            for n, option in enumerate(options):
                if option[1] < 0 or option[1] > board_size - 1:
                    continue
                else:
                    if board[option[0]][option[1]] != 0:
                        if board[option[0]][option[1]].color == self.color:
                            continue
                        else:
                            if self.row + 2 > board_size - 1:
                                continue
                            else:
                                if n == 0:
                                    if self.col - 2 < 0:
                                        continue
                                    else:
                                        if board[option[0] + 1][option[1] - 1] != 0:
                                            continue
                                        else:
                                            checked_options.append([(option[0] + 1, option[1] - 1),
                                                                    board[option[0]][option[1]]])
                                else:
                                    if self.col + 2 > board_size - 1:
                                        continue
                                    else:
                                        if board[option[0] + 1][option[1] + 1] != 0:
                                            continue
                                        else:
                                            checked_options.append([(option[0] + 1, option[1] + 1),
                                                                    board[option[0]][option[1]]])
                    else:
                        checked_options.append([option, 0])
        return checked_options

    def move(self, board, option):
        board[self.row][self.col] = 0
        board[option[0]][option[1]] = self
        self.row = option[0]
        self.col = option[1]

    def __str__(self):
        return colored(self.num, self.color)

    def __repr__(self):
        return colored(self.num, self.color)


class Player:

    def __init__(self, color):
        self.color = color
        self.soldiers = []
        n = 1
        if color == p1_color:
            for i in range(board_size - 3, board_size):
                for j in range(board_size):
                    if i % 2 == 1 and j % 2 == 1:
                        self.soldiers.append(Soldier(color, i, j, n))
                        n += 1
                    elif i % 2 == 0 and j % 2 == 0:
                        self.soldiers.append(Soldier(color, i, j, n))
                        n += 1
        else:
            for i in range(0, 3):
                for j in range(board_size):
                    if i % 2 == 1 and j % 2 == 1:
                        self.soldiers.append(Soldier(color, i, j, n))
                        n += 1
                    elif i % 2 == 0 and j % 2 == 0:
                        self.soldiers.append(Soldier(color, i, j, n))
                        n += 1

    def can_i_play(self, board):
        for sol in self.soldiers:
            if sol.check_move(board):
                return True
        return False

    def search_player(self, num):
        list_num = [sol.num for sol in self.soldiers]
        index = list_num.index(num)
        return self.soldiers[index]

    def check_move(self, board, num):
        if not self.can_i_play(board):
            return False
        sol = self.search_player(num)
        return sol.check_move(board)

    def move(self, board, num, checked_moves, option_index):
        option = checked_moves[option_index][0]
        sol = self.search_player(num)
        sol.move(board, option)

    def delete_sol(self, board, sol):
        board[sol.row][sol.col] = 0
        self.soldiers.remove(sol)

    def __str__(self):
        return self.soldiers.__str__()

    def __repr__(self):
        return self.soldiers.__repr__()


class Manager:

    def __init__(self):
        self.board = create_board(board_size)
        self.p1 = Player(p1_color)
        self.p2 = Player(p2_color)
        for sol in self.p1.soldiers + self.p2.soldiers:
            self.board[sol.row][sol.col] = sol
        self.n = 0
        self.chance_for_draw = 0

    def check_win(self, num):
        if self.n % 2 == 0:
            sol = self.p1.search_player(num)
            if not self.p2.soldiers:
                return True
            if sol.row == 0:
                return True
        else:
            sol = self.p2.search_player(num)
            if not self.p1.soldiers:
                return True
            if sol.row == board_size - 1:
                return True
        return False

    def turn(self):
        colors = [p1_color, p2_color]
        options = []
        num = -1
        if self.n % 2 == 0:
            if not self.p1.can_i_play(self.board):
                if not self.chance_for_draw:
                    self.chance_for_draw = 1
                    print(f"The {colors[self.n % 2]} player cannot play")
                    self.n += 1
                    return
                else:
                    print("This match is a draw")
                    exit(0)
            else:
                if self.chance_for_draw == 1:
                    self.chance_for_draw = 0
        else:
            if not self.p2.can_i_play(self.board):
                if not self.chance_for_draw:
                    self.chance_for_draw = 1
                    print(f"The {colors[self.n % 2]} player cannot play")
                    self.n += 1
                    return
                else:
                    print("This match is a draw")
                    exit(0)
            else:
                if self.chance_for_draw == 1:
                    self.chance_for_draw = 0
        while True:
            print_board(self.board)
            num = input(f"This is {colors[self.n % 2]}'s turn. pick a {colors[self.n % 2]} number\n")
            if num.isnumeric():
                num = int(num)
            else:
                print("Enter a number")
                continue
            if self.n % 2 == 0:
                if num not in [sol.num for sol in self.p1.soldiers]:
                    print(f"{num} not in {colors[self.n % 2]}'s list")
                    continue
            else:
                if num not in [sol.num for sol in self.p2.soldiers]:
                    print(f"{num} not in {colors[self.n % 2]}'s list")
                    continue
            if self.n % 2 == 0:
                options = self.p1.check_move(self.board, num)
                if options == []:
                    print(f"{num} has no option to go to")
                    continue
                for i, option in enumerate(options):
                    self.board[option[0][0]][option[0][1]] = i + 1
                break
            else:
                options = self.p2.check_move(self.board, num)
                if options == []:
                    print(f"{num} has no option to go to")
                    continue
                for i, option in enumerate(options):
                    self.board[option[0][0]][option[0][1]] = i + 1
                break
        while True:
            print_board(self.board)
            pick = input(f"select one of the {choice_color} options to make\n")
            if pick.isnumeric():
                pick = int(pick) - 1
                if pick not in range(len(options)):
                    print("This option is incorrect")
                    continue
            else:
                print("Enter a number")
                continue
            if pick not in range(len(options)):
                print("This pick is not optional")
                continue
            if self.n % 2 == 0:
                self.p1.move(self.board, num, options, pick)
                if options[pick][1] != 0:
                    self.p2.delete_sol(self.board, options[pick][1])
            else:
                self.p2.move(self.board, num, options, pick)
                if options[pick][1] != 0:
                    self.p1.delete_sol(self.board, options[pick][1])
            for option in options:
                if option != options[pick]:
                    self.board[option[0][0]][option[0][1]] = 0
            if self.check_win(num):
                print_board(self.board)
                print(f"{colors[self.n % 2]} is the winner!!!")
                exit(0)
            else:
                self.n += 1
                return

    def play(self):
        while True:
            self.turn()


def print_board(board):
    for row in board:
        for j in row:
            if type(j) != Soldier and j != 0 and j != '-':
                print(colored(j, choice_color), end=" ")
            else:
                print(j, end=" ")
        print("\n")


def create_board(board_size):
    board1 = []
    for i in range(board_size):
        row_i = []
        for j in range(board_size):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                row_i.append(0)
            else:
                row_i.append("-")
        board1.append(row_i)
    return board1


man = Manager()
man.play()
'''
p1 = Player(p1_color)
p2 = Player(p2_color)
board1 = create_board(board_size)
for sol in p1.soldiers + p2.soldiers:
    board1[sol.row][sol.col] = sol
print_board(board1)
'''


'''
sol1 = Soldier(p1_color, 7, 1, 10)
sol2 = Soldier(p2_color, 6, 6, 6)

board1 = create_board(board_size)
board1[sol1.row][sol1.col] = sol1
board1[sol2.row][sol2.col] = sol2
print_board(board1)
print(sol2.check_move(board1))
'''