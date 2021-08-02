import random
import copy
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']

    def succ(self, state, player):  # ?????

        if player == 'my':
            tile = self.my_piece
        if player == 'opp':
            tile = self.opp

        drop_phase = True
        # TODO: detect drop phase
        count = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] != ' ':
                    count = count + 1
        if count >= 8:
            drop_phase = False

        successor = []
        if drop_phase:
            # print('1111')
            for row in range(5):
                for col in range(5):
                    if state[row][col] == ' ':
                        successor.append(self.drop(state, row, col, tile))
        if not drop_phase:
            for row in range(5):
                for col in range(5):
                    if state[row][col] == tile:
                        if 0 <= (row - 1) <= 4 and 0 <= (col - 1) <= 4:  # 1
                            if state[row - 1][col - 1] == ' ':
                                successor.append(self.switch(state, row, col, row - 1, col - 1, tile))
                        if 0 <= (row - 1) <= 4:  # 2
                            if state[row - 1][col] == ' ':
                                successor.append(self.switch(state, row, col, row - 1, col, tile))
                        if 0 <= (row - 1) <= 4 and 0 <= (col + 1) <= 4:  # 3
                            if state[row - 1][col + 1] == ' ':
                                successor.append(self.switch(state, row, col, row - 1, col + 1, tile))
                        if 0 <= (col - 1) <= 4:  # 4
                            if state[row][col - 1] == ' ':
                                successor.append(self.switch(state, row, col, row, col - 1, tile))
                        if 0 <= (col + 1) <= 4:  # 6
                            if state[row][col + 1] == ' ':
                                successor.append(self.switch(state, row, col, row, col + 1, tile))
                        if 0 <= (row + 1) <= 4 and 0 <= (col - 1) <= 4:  # 7
                            if state[row + 1][col - 1] == ' ':
                                successor.append(self.switch(state, row, col, row + 1, col - 1, tile))
                        if 0 <= (row + 1) <= 4:  # 8
                            if state[row + 1][col] == ' ':
                                successor.append(self.switch(state, row, col, row + 1, col, tile))
                        if 0 <= (row + 1) <= 4 and 0 <= (col + 1) <= 4:  # 9
                            if state[row + 1][col + 1] == ' ':
                                successor.append(self.switch(state, row, col, row + 1, col + 1, tile))
        return successor

    def drop(self, state, row, col, tile):  # ??????
        newboard = copy.deepcopy(state)
        newboard[row][col] = tile
        # print(state)
        return newboard

    def switch(self, state, row, col, row1, col1, tile):  # ??????
        newboard = copy.deepcopy(state)
        newboard[row][col] = ' '
        newboard[row1][col1] = tile
        return newboard

    def heuristic_game_value(self, state):
        value = self.game_value(state)
        if value != 0:
            return float(value)

        win_count = 0
        lose_count = 0

        tile = self.my_piece
        untile = self.opp


#########################
        for x in range(5):
            for y in range(5):
                # check horizontal spaces
                if x<2:
                    if (state[x][y] == tile or state[x][y] == ' ') and \
                            (state[x + 1][y] == tile or state[x + 1][y] == ' ') and \
                            (state[x + 2][y] == tile or state[x + 2][y] == ' ') and \
                            (state[x + 3][y] == tile or state[x + 3][y] == ' '):
                        win_count += 1

                    if (state[x][y] == untile or state[x][y] == ' ') and \
                            (state[x + 1][y] == untile or state[x + 1][y] == ' ') and \
                            (state[x + 2][y] == untile or state[x + 2][y] == ' ') and \
                            (state[x + 3][y] == untile or state[x + 3][y] == ' '):
                        lose_count += 1
                # check vertical spaces
                if y<2:
                    if (state[x][y] == tile or state[x][y] == ' ') and \
                            (state[x][y + 1] == tile or state[x][y + 1] == ' ') and \
                            (state[x][y + 2] == tile or state[x][y + 2] == ' ') and \
                            (state[x][y + 3] == tile or state[x][y + 3] == ' '):
                        win_count += 1
                    if (state[x][y] == untile or state[x][y] == ' ') and \
                            (state[x][y + 1] == untile or state[x][y + 1] == ' ') and \
                            (state[x][y + 2] == untile or state[x][y + 2] == ' ') and \
                            (state[x][y + 3] == untile or state[x][y + 3] == ' '):
                        lose_count += 1
                # check \ diagonal spaces
                if x<2 and y<2:
                    if (state[x][y] == tile or state[x][y] == ' ') and \
                            (state[x + 1][y + 1] == tile or state[x + 1][y + 1] == ' ') and \
                            (state[x + 2][y + 2] == tile or state[x + 2][y + 2] == ' ') and \
                            (state[x + 3][y + 3] == tile or state[x + 3][y + 3] == ' '):
                        win_count += 1
                    if (state[x][y] == untile or state[x][y] == ' ') and \
                            (state[x + 1][y + 1] == untile or state[x + 1][y + 1] == ' ') and \
                            (state[x + 2][y + 2] == untile or state[x + 2][y + 2] == ' ') and \
                            (state[x + 3][y + 3] == untile or state[x + 3][y + 3] == ' '):
                        lose_count += 1
                # check / diagonal spaces
                if x<2 and 3<=y<5:
                    if (state[x][y] == tile or state[x][y] == ' ') and \
                            (state[x + 1][y - 1] == tile or state[x + 1][y - 1] == ' ') and \
                            (state[x + 2][y - 2] == tile or state[x + 2][y - 2] == ' ') and \
                            (state[x + 3][y - 3] == tile or state[x + 3][y - 3] == ' '):
                        win_count += 1
                    if (state[x][y] == untile or state[x][y] == ' ') and \
                            (state[x + 1][y - 1] == untile or state[x + 1][y - 1] == ' ') and \
                            (state[x + 2][y - 2] == untile or state[x + 2][y - 2] == ' ') and \
                            (state[x + 3][y - 3] == untile or state[x + 3][y - 3] == ' '):
                        lose_count += 1
                # check 2x2 box wins
                if x<4 and y<4:
                    if (state[x][y] == tile or state[x][y] == ' ') and \
                            (state[x + 1][y + 1] == tile or state[x + 1][y + 1] == ' ') and \
                            (state[x + 1][y] == tile or state[x + 1][y] == ' ') and \
                            (state[x][y + 1] == tile or state[x][y + 1] == ' '):
                        win_count += 1
                    if (state[x][y] == untile or state[x][y] == ' ') and \
                            (state[x + 1][y + 1] == untile or state[x + 1][y + 1] == ' ') and \
                            (state[x + 1][y] == untile or state[x + 1][y] == ' ') and \
                            (state[x][y + 1] == untile or state[x][y + 1] == ' '):
                        lose_count += 1


        ##    print "heuristic: ", win_count, lose_count, win_count - lose_count/total possibility to win
        return float((win_count - lose_count) / (16 + 20 + 8))

    def Max_Value(self, state, depth):
        if self.game_value(state) != 0:
            return self.game_value(state)
        if depth == 2:
            return self.heuristic_game_value(state)
        else:
            score = float('-inf')
            successors = self.succ(state, 'my')
            for succ in successors:
                cur = self.Min_Value(succ, depth + 1)
                score = max(score, cur)
            return score

    def Min_Value(self, state, depth):
        if self.game_value(state) != 0:
            return self.game_value(state)
        if depth == 2:
            return self.heuristic_game_value(state)
        else:
            score = float('inf')
            successors = self.succ(state, 'opp')
            for succ in successors:
                cur = self.Max_Value(succ, depth + 1)
                score = min(score, cur)
            return score


    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.
            
        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.
                
                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).
        
        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        t=time.time()
        drop_phase = True
        # TODO: detect drop phase
        count = 0
        for i in range(5):
            for j in range(5):
                if state[i][j] == ' ':
                    count = count + 1
        if count >= 8:
            drop_phase = False

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
        move = []

        succeccer = []
        succeccer = self.succ(self.board, 'my')
        # print(succeccer)
        h = []
        for ss in succeccer:
            h.append(self.Max_Value(ss, 0))
        # print(h)
        max = -10
        index = 0
        for i in range(len(h)):
            if h[i] > max:
                max = h[i]
                index = i

        max_move = succeccer[index]
        # print(max_move)
        (row, col) = (0, 0)
        if drop_phase:
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] != max_move[i][j]:
                        (row, col) = (i, j)
        # [(row, col), (source_row, source_col)]
        if not drop_phase:
            for i in range(5):
                for j in range(5):
                    if self.board[i][j] != max_move[i][j] and self.board[i][j] == ' ':
                        (row, col) = (i, j)
                    if self.board[i][j] != max_move[i][j] and self.board[i][j] == self.my_piece:
                        (source_row, source_col) = (i, j)
                        move.append((source_row, source_col))

        # (row, col) = (random.randint(0, 4), random.randint(0, 4))
        # while not state[row][col] == ' ':
        # (row, col) = (random.randint(0, 4), random.randint(0, 4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        move.insert(0, (row, col))
        print(time.time() - t)
        return move

    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                raise Exception("You don't have a piece there!")
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece
        
        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
                
                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row) + ": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition
        
        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and 2x2 box wins
        """
        # check horizontal wins
        for row in state:
            for i in range(2):
                if row[i] != ' ' and row[i] == row[i + 1] == row[i + 2] == row[i + 3]:
                    return 1 if row[i] == self.my_piece else -1

        # check vertical wins
        for col in range(5):
            for i in range(2):
                if state[i][col] != ' ' and state[i][col] == state[i + 1][col] == state[i + 2][col] == state[i + 3][
                    col]:
                    return 1 if state[i][col] == self.my_piece else -1

        # TODO: check \ diagonal wins
        for i in range(2):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j + 1] == state[i + 2][j + 2] == state[i + 3][
                    j + 3]:
                    return 1 if state[i][j] == self.my_piece else -1
        # TODO: check / diagonal wins
        for i in range(3, 5):
            for j in range(2):
                if state[i][j] != ' ' and state[i][j] == state[i - 1][j - 1] == state[i - 2][j - 2] == state[i - 3][
                    j - 3]:
                    return 1 if state[i][j] == self.my_piece else -1

        # TODO: check 2x2 box wins
        for i in range(4):
            for j in range(4):
                if state[i][j] != ' ' and state[i][j] == state[i + 1][j + 1] == state[i + 1][j] == state[i][j + 1]:
                    return 1 if state[i][j] == self.my_piece else -1

        return 0  # no winner yet


############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################

ai = TeekoPlayer()
piece_count = 0
turn = 0

# drop phase
while piece_count < 8:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece + " moved at " + chr(move[0][1] + ord("A")) + str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp + "'s turn")
        while not move_made:
            player_move = input("Move (e.g. B3): ")
            while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                player_move = input("Move (e.g. B3): ")
            try:
                ai.opponent_move([(int(player_move[1]), ord(player_move[0]) - ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    piece_count += 1
    turn += 1
    turn %= 2

# move phase - can't have a winner until all 8 pieces are on the board
while ai.game_value(ai.board) == 0:

    # get the player or AI's move
    if ai.my_piece == ai.pieces[turn]:
        ai.print_board()
        move = ai.make_move(ai.board)
        ai.place_piece(move, ai.my_piece)
        print(ai.my_piece + " moved from " + chr(move[1][1] + ord("A")) + str(move[1][0]))
        print("  to " + chr(move[0][1] + ord("A")) + str(move[0][0]))
    else:
        move_made = False
        ai.print_board()
        print(ai.opp + "'s turn")
        while not move_made:
            move_from = input("Move from (e.g. B3): ")
            while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                move_from = input("Move from (e.g. B3): ")
            move_to = input("Move to (e.g. B3): ")
            while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                move_to = input("Move to (e.g. B3): ")
            try:
                ai.opponent_move([(int(move_to[1]), ord(move_to[0]) - ord("A")),
                                  (int(move_from[1]), ord(move_from[0]) - ord("A"))])
                move_made = True
            except Exception as e:
                print(e)

    # update the game variables
    turn += 1
    turn %= 2

ai.print_board()
if ai.game_value(ai.board) == 1:
    print("AI wins! Game over.")
else:
    print("You win! Game over.")
