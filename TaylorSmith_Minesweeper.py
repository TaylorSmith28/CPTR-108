import random
import re
import math


class Board:

    def __init__(self, num_row, num_col, num_bombs):
      # Constructor Funtion to set board data
        self.num_row = num_row
        self.num_col = num_col
        self.num_bombs = num_bombs
        self.board = self.make_board()
        self.set_flags()
        self.dug = set()

    def make_board(self):
      # Creates a board by placing bombs on the board and values for nearby bombs.
        board = [[None for _ in range(self.num_col)]
                 for _ in range(self.num_row)]
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.num_row*self.num_col-1)
            row = math.floor(loc / self.num_col)
            col = loc % self.num_col
            if board[row][col] != '*':
                board[row][col] = "*"
                bombs_planted += 1
        return board

    def set_flags(self):
        for r in range(self.num_row):
            for c in range(self.num_col):
                if self.board[r][c] != '*':
                    self.board[r][c] = self.check_adjacent_bombs(r, c)

    def check_adjacent_bombs(self, row, col):
      # Checks for adjancent bombs
        bombs = 0
        for r in range(max(0, row-1), min(self.num_row-1, (row+1))+1):
            for c in range(max(0, col-1), min(self.num_col-1, col+1)+1):
                if ((self.board[r][c] == '*') and not (r == row and c == col)):
                    bombs += 1
        return bombs

    def dig(self, row, col):
        # Checks where you dug and all nearby areas
        self.dug.add((row, col))
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        for r in range(max(0, row-1), min(self.num_row-1, (row+1))+1):
            for c in range(max(0, col-1), min(self.num_col-1, col+1)+1):
                if (r, c) in self.dug:
                    continue
                self.dig(r, c)
        return True

    def save_game(self):
        with open("savegame.txt", "w") as f:
            for row in self.board:
                f.write(''.join([str(a) for a in row]) + '\n')
        with open("savedata.txt", "w") as f:
            f.write(str(self.num_row) + '\n')
            f.write(str(self.num_col) + '\n')
            f.write(str(self.num_bombs) + '\n')
        with open("savedugsquares.txt", "w") as f:
            f.write(str(self.dug))

    def load_game(self):
        with open("savegame.txt", "rt") as f:
            self.board = [list(line.strip()) for line in f.readlines()]
        with open("savedata.txt", "rt") as f:
            self.num_row = (f.readline())
            self.num_row = int(self.num_row)
            self.num_col = (f.readline())
            self.num_col = int(self.num_col)
            self.num_bombs = (f.readline())
            self.num_bombs = int(self.num_bombs)
        # with open("savevisible.txt", "rt") as f:
            # Was unable to determine how to load the visible board.

    def __str__(self):
        visible_board = [[None for _ in range(
            self.num_col)] for _ in range(self.num_row)]
        for row in range(self.num_row):
            for col in range(self.num_col):
                if(row, col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '

        # Formatting
        # Used Code_Camp to help with formatting of the board
        string_rep = ''
        widths = []
        for idx in range(self.num_col):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key=len)
                )
            )

        indices = [i for i in range(self.num_col)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.num_row)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play():
    running = True
    while(running):
        while(True):
            user_input = input(
                "Normal Game, Custom Game, or Load Game (N or C or L): ")
            if (user_input == "c") or (user_input == "C"):
                # Ask for Dimensions and Number of Bombs
                num_row = int(input("Number of Rows: "))
                num_col = int(input("Number of Colums: "))
                num_bombs = int(input("Number of Bombs: "))
                break
            elif (user_input == "n") or (user_input == "N"):
                num_row = 10
                num_col = 10
                num_bombs = 10
                break
            elif (user_input == "l") or (user_input == "L"):
                num_row = 10
                num_col = 10
                num_bombs = 10
                break
            else:
                print("Invalid input, try again")

        # Create the board and place bombs
        board = Board(num_row, num_col, num_bombs)
        if(user_input == "l") or (user_input == "L"):
            board.load_game()

        # Show player the board and ask where they want to dig
        # if location is bomb, game over if location is not a bomb, dig until each square is at least next to  bomb
        safe = True
        while len(board.dug) < board.num_col * num_row - num_bombs:
            print(board)
            print("Where would you like to dig?")
            row = input("Row: ")
            col = input("Col: ")
            if (row == "q" or row == "Q" or col == "q" or col == "Q"):
                while(True):
                    user_input = input(
                        "Would you like to save first (y or n): ")
                    if(user_input == "y") or (user_input == "Y"):
                        print("Game Saved!")
                        board.save_game()
                        exit()
                    elif(user_input == "n") or (user_input == "N"):
                        print("Thanks for playing!")
                        exit()
                    else:
                        print("Invalid Input")
            if (row == "s" or row == "S" or col == "S" or col == "s"):
                board.save_game()
                print("Game Saved!")
                row = int(-1)
                col = int(-1)
            if (row == "L" or row == "l" or col == "L" or col == "l"):
                board.save_game()
                print("Game loaded!")
                row = int(-1)
                col = int(-1)
            row = int(row)
            col = int(col)
            if row < 0 or row >= board.num_row or col < 0 or col >= board.num_col:
                print("Invalid location. Try again.")
                continue

            safe = board.dig(row, col)
            if not safe:
                break

        # Win Condition
        if safe:
            print("You Won!!!")
            print(board)
            while(True):
                user_input = input("Play again (y or n): ")
                if (user_input == "n") or (user_input == "N"):
                    running = False
                    break
                elif (user_input == "y") or (user_input == "Y"):
                    running = True
                    break
                else:
                    print("Invalid input.")

        # Lose Condition
        else:
            print("Game Over")
            board.dug = [(r, c) for r in range(board.num_row)
                         for c in range(board.num_col)]
            print(board)
            while(True):
                user_input = input("Play again (y or n): ")
                if (user_input == "n") or (user_input == "N"):
                    running = False
                    break
                elif (user_input == "y") or (user_input == "Y"):
                    running = True
                    break
                else:
                    print("Invalid input.")

    print("Thanks for playing!")


if __name__ == '__main__':
    play()
