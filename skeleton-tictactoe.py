import random
import time
import numpy as np


class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, recommend=True, size=3, blocs=0, bloc_pos=[], win_val=3, time=3, d1=3, d2=3):
        self.board_size = size
        self.blocs = blocs
        self.bloc_pos = bloc_pos
        self.win_val = win_val
        self.initialize_game()
        self.recommend = recommend
        self.d1 = d1
        self.d2 = d2
        self.time = time

    def initialize_game(self):
        self.current_state = []
        self.depth = 0
        for x in range(0, self.board_size):
            self.current_state.append([])
            for y in range(0, self.board_size):
                found = False
                for z in self.bloc_pos:
                    if x == z[0] and y == z[1]:
                        self.current_state[x].append('<>')
                        found = True
                if not found:
                    self.current_state[x].append('.')
        # Player X always plays first
        self.player_turn = 'X'

    def draw_board(self):
        self.depth = 0
        print()
        for x in range(0, self.board_size):
            for y in range(0, self.board_size):
                print(F'{self.current_state[x][y]}', end="\t")
            print()
        print()

    def is_valid(self, px, py):
        if px < 0 or px > self.board_size - 1 or py < 0 or py > self.board_size - 1:
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def is_end(self):
        if self.win_val == self.board_size:
            # Vertical win
            for i in range(0, self.board_size):
                base_symbol = self.current_state[0][i]
                win = False
                for j in range(1, self.board_size):
                    if (self.current_state[j][i] == base_symbol and
                            base_symbol != '.' and
                            base_symbol != '<>'):
                        win = True
                    else:
                        win = False
                        break
                if win:
                    return base_symbol
            # Horizontal win
            for i in range(0, self.board_size):
                if self.current_state[i].count('X') == self.board_size:
                    return 'X'
                elif self.current_state[i].count('O') == self.board_size:
                    return 'O'
            # Main diagonal win
            corner_symbol = self.current_state[0][0]
            win = False
            for i in range(1, self.board_size):
                if (self.current_state[i][i] == corner_symbol and
                        corner_symbol != '.' and
                        corner_symbol != '<>'):
                    win = True
                else:
                    win = False
                    break
            if win:
                return corner_symbol
            # Second diagonal win
            corner_symbol = self.current_state[0][self.board_size - 1]
            win = False
            for i in range(1, self.board_size):
                for j in range(self.board_size - 2, 0):
                    if (self.current_state[i][j] == corner_symbol and
                            corner_symbol != '.' and
                            corner_symbol != '<>'):
                        win = True
                        break
                    else:
                        win = False
                        break
            if win:
                return corner_symbol
        else:
            # Vertical
            win = False
            for i in range(0, self.board_size):
                for j in range(0, self.board_size):
                    current = self.current_state[i][j]
                    win = False
                    if i + 1 < self.board_size and i + self.win_val < self.board_size:
                        for x in range(i + 1, i + self.win_val + 1):
                            if ((self.board_size - 1 - i) >= self.win_val and
                                    self.current_state[x][j] == current and
                                    current != '.' and
                                    current != '<>'):
                                win = True
                            else:
                                win = False
                                break
                        if win:
                            return current

            # Horizontal
            win = False
            for i in range(0, self.board_size):
                for j in range(0, self.board_size):
                    current = self.current_state[i][j]
                    if j + 1 < self.board_size and j + self.win_val < self.board_size:
                        for x in range(j + 1, j + self.win_val + 1):
                            if ((self.board_size - 1 - j) >= self.win_val and
                                    self.current_state[i][x] == current and
                                    current != '.' and
                                    current != '<>'):
                                win = True
                            else:
                                win = False
                                break
                        if win:
                            return current

            # Main diagonal
            win = False
            for i in range(0, self.board_size):
                for j in range(0, self.board_size):
                    current = self.current_state[i][j]
                    if i + 1 < self.board_size and i + self.win_val < self.board_size and j + 1 < self.board_size:
                        index = j
                        for x in range(i + 1, i + self.win_val + 1):
                            if index + 1 < self.board_size:
                                index += 1
                            if ((self.board_size - 1 - i) >= self.win_val and
                                    self.current_state[x][index] == current and
                                    current != '.' and
                                    current != '<>'):
                                win = True
                            else:
                                win = False
                                break
                        if win:
                            return current
            # Other diagonal
            win = False
            for i in range(0, self.board_size):
                for j in range(self.board_size - 1, -1):
                    current = self.current_state[i][j]
                    if i + 1 < self.board_size and i + self.win_val < self.board_size and j - 1 >= 0:
                        index = j
                        for x in range(i + 1, i + self.win_val + 1):
                            if index - 1 > 0:
                                index -= 1
                            if ((self.board_size - 1 - i) >= self.win_val and
                                    self.current_state[x][index] == current and
                                    current != '.' and
                                    current != '<>'):
                                win = True
                            else:
                                win = False
                                break
                        if win:
                            return current
        # print("here")
        # Is whole board full?
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
            elif self.result == 'O':
                print('The winner is O!')
            elif self.result == '.':
                print("It's a tie!")
            self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        self.depth = 0
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    # Implementing e1

    def e1(self, max):
        h = 0
        # check h in each row
        for i in range(0, self.board_size):
            num_x = 0
            num_o = 0
            for j in range(0, self.board_size):
                if self.current_state[i][j] == "X":
                    num_x += 1
                if self.current_state[i][j] == "O":
                    num_o += 1
            h += num_x * self.win_val
            h -= num_o * self.win_val

        # check columns
        for j in range(0, self.board_size):
            num_x = 0
            num_o = 0
            for i in range(0, self.board_size):
                if self.current_state[i][j] == "X":
                    num_x += 1
                if self.current_state[i][j] == "O":
                    num_o += 1
            h += num_x * self.win_val
            h -= num_o * self.win_val
        # # check right-tilt diagonals

        for i in range(-(self.board_size - 1), self.board_size):
            count_array = np.diag(self.current_state, k=i)
            num_x = 0
            num_o = 0

            for j in range(0, len(count_array)):
                if count_array[j] == "X":
                    num_x += 1

                if count_array[j] == "O":
                    num_o += 1
            h += num_x * self.win_val
            h -= num_o * self.win_val

        # # checking left-tilt diagonals
        for i in range(-(self.board_size - 1), self.board_size):
            count_array = np.diag((np.fliplr(self.current_state)), k=i)
            num_x = 0
            num_o = 0

            for j in range(0, len(count_array)):
                if count_array[j] == "X":
                    num_x += 1
                if count_array[j] == "O":
                    num_o += 1
            h += num_x * self.win_val
            h -= num_o * self.win_val

        return h

    def e2(self, max):
        h = 0
        # check h in each row
        for i in range(0, self.board_size):
            num_x = 0
            num_o = 0
            for j in range(0, self.board_size-1):
                if self.current_state[i][j] == "X":
                    if self.current_state[i][j+1] == '.':
                        num_x += 2
                    else:
                        num_x += 1
                if self.current_state[i][j] == "O":
                    if self.current_state[i][j+1] == '.':
                        num_o += 2
                    else:
                        num_o += 1
            h += num_x
            h -= num_o

        # check columns
        for j in range(0, self.board_size-1):
            num_x = 0
            num_o = 0
            for i in range(0, self.board_size):
                if self.current_state[i][j] == "X":
                    if self.current_state[i][j+1] == '.':
                        num_x += 2
                    else:
                        num_x += 1
                if self.current_state[i][j] == "O":
                    if self.current_state[i][j+1] == '.':
                        num_o += 2
                    else:
                        num_o += 1
            h += num_x
            h -= num_o
        # # check right-tilt diagonals

        for i in range(-(self.board_size - 1), self.board_size):
            count_array = np.diag(self.current_state, k=i)
            num_x = 0
            num_o = 0

            for j in range(0, len(count_array)-1):
                if count_array[j] == "X":
                    if count_array[j+1] == '.':
                        num_x += 2
                    else:
                        num_x += 1
                if count_array[j] == "O":
                    if count_array[j+1] == '.':
                        num_o += 2
                    else:
                        num_o += 1
            h += num_x
            h -= num_o

        # # checking left-tilt diagonals
        for i in range(-(self.board_size - 1), self.board_size):
            count_array = np.diag((np.fliplr(self.current_state)), k=i)
            num_x = 0
            num_o = 0

            for j in range(0, len(count_array)-1):
                if count_array[j] == "X":
                    if count_array[j+1] == '.':
                        num_x += 2
                    else:
                        num_x += 1
                if count_array[j] == "O":
                    if count_array[j+1] == '.':
                        num_o += 2
                    else:
                        num_o += 1
            h += num_x
            h -= num_o
        if max:
            return h+ (-2 - h)
        else:
            return h-(h-2)

    def minimax(self, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()

        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        elif self.player_turn == 'X' and self.depth >= self.d1:
            return (self.e2(max=max), x, y)
        elif self.player_turn == 'O' and self.depth >= self.d2:
            return (self.e2(max=max), x, y)
        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'

        if (self.player_turn == 'X' and self.depth < self.d1) or (self.player_turn == 'O' and self.depth < self.d2):
            self.depth += 1

        return (value, x, y)

    def alphabeta(self, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()

        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        elif self.player_turn == 'X' and self.depth >= self.d1:
            return (self.e1(max=max), x, y)
        elif self.player_turn == 'O' and self.depth >= self.d2:
            return (self.e1(max=max), x, y)

        for i in range(0, self.board_size):
            for j in range(0, self.board_size):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(alpha, beta, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j

                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value

        if (self.player_turn == 'X' and self.depth < self.d1) or (self.player_turn == 'O' and self.depth < self.d2):
            self.depth += 1

        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(max=False)
                else:
                    (_, x, y) = self.minimax(max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(
                    F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()


def set_bloc_pos(bloc_size, board_size):
    bloc_tuple_list = []

    for i in range(0, bloc_size):
        found = False
        while not found:
            bloc_x = random.randint(0, board_size - 1)
            bloc_y = random.randint(0, board_size - 1)
            new_bloc = (bloc_x, bloc_y)

            if bloc_tuple_list.count(new_bloc) == 0:
                bloc_tuple_list.append(new_bloc)
                found = True
    return bloc_tuple_list


def main():
    size = random.randint(3, 7)
    # 3
    blocs = random.randint(0, 2 * size)
    # 0
    bloc_positions = set_bloc_pos(blocs, size)

    # []
    winning_values = random.randint(3, size)
    # 3
    max_depth_1 = random.randint(3, size)
    max_depth_2 = max_depth_1
    g = Game(recommend=True, size=size, blocs=blocs, bloc_pos=bloc_positions, win_val=winning_values, d1=max_depth_1,
             d2=max_depth_2)
    g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)
    #g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.AI)


if __name__ == "__main__":
    main()
