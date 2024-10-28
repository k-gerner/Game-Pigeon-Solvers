# Kyle Gerner    7.9.2020


# class that represents the Player (of which, there are 2)
class AvalanchePlayer(object):
    def __init__(self):
        self.score = 0

    def increment_score(self):
        self.score += 1

    def copy_player(self):
        p = AvalanchePlayer()
        p.score = self.score
        return p

################################################################################################
################################################################################################
################################################################################################


BANK = 0
EMPTY_PIT = 1
PIT_WITH_PIECES = 2


# Class that represents the board object.
class AvalancheBoard(object):

    # constructor
    def __init__(self, pebbles_in_each, player1, player2, player_one_turn):
        self.pebblesList = pebbles_in_each.copy()
        self.p1 = player1
        self.p2 = player2
        self.p1Turn = player_one_turn

    # Performs the moves on the board by calling the perform_move function for each move given
    def perform_move_set(self, move_list):
        continue_moves = True
        move_number = 1
        for boardSpot in move_list:
            if not continue_moves:
                print("Move #%d in the given move set was invalid (previous move did not end in player bank)" % move_number)
                print("The move set was:  " + str(move_list))
                break
            continue_moves = self.perform_move(boardSpot)
            move_number += 1
        self.switch_turn()
        return self.p1.score, self.p2.score

    # Performs the move on the board
    def perform_move(self, position):
        curr_bank_index, enemy_bank_index = self.get_bank_indexes()
        curr_player = self.p1 if self.p1Turn else self.p2
        num_pebbles = self.pebblesList[position]
        self.pebblesList[position] = 0
        turn_ended_in_player_bank = False
        while True:
            if num_pebbles == 0:
                end_of_move = self.end_of_current_move(position, curr_bank_index)
                if end_of_move != PIT_WITH_PIECES:
                    turn_ended_in_player_bank = True if end_of_move == BANK else False
                    break
                else:
                    num_pebbles = self.pebblesList[position]
                    self.pebblesList[position] = 0
            position = (position + 1) % 14 if (position + 1) != enemy_bank_index else (position + 2) % 14
            self.add_pebble_to_location(position, curr_bank_index, curr_player)
            num_pebbles -= 1
        return turn_ended_in_player_bank

    # checks which spot the last piece was placed
    def end_of_current_move(self, pos, curr_bank_index):
        # note if this method is called, we already know numPebbles = 0
        if pos == curr_bank_index:
            return BANK
        elif self.pebblesList[pos] == 1:
            return EMPTY_PIT
        else:
            return PIT_WITH_PIECES

    # places a piece in the specified spot, and increments score if applicable
    def add_pebble_to_location(self, index, curr_bank_index, curr_player):
        self.pebblesList[index] += 1
        if index == curr_bank_index:
            curr_player.increment_score()

    # get the player and opponent bank indexes
    def get_bank_indexes(self):
        if self.p1Turn:
            return 6, 13
        else:
            return 13, 6

    # prints the board in a horizontal fashion
    def print_board_horizontal(self):
        #  E  |12 |11 |10 | 9 | 8 | 7 |
        # 13  -------------------------  6
        #     | 0 | 1 | 2 | 3 | 4 | 5 |  P
        #      Enemy winning 13 to 6
        if self.p2.score == self.p1.score:
            score_str = "\t  The score is tied at %d\n" % self.p2.score
        else:
            if self.p2.score > self.p1.score:
                score_str = "\t  Enemy winning %d to %d\n" % (self.p2.score, self.p1.score)
            else:
                score_str = "\t  You're winning %d to %d\n" % (self.p1.score, self.p2.score)
        print(str(self) + score_str)

    # string representation of the board
    def __str__(self):
        enemy_row = "E\t|" + self.score_row_to_str_horiz(12, 6, -1) + "\n"
        bank_row = "%d\t-------------------------\t%d\n" % (self.p2.score, self.p1.score)
        player_row = "\t|" + self.score_row_to_str_horiz(0, 6, 1) + "\tP\n"
        return enemy_row + bank_row + player_row

    # string representation of one side of the board
    def score_row_to_str_horiz(self, start, end, direction):
        scores_str = ""
        for i in range(start, end, direction):  # loop thru indexes of side
            this_spot_str = "%d |" % self.pebblesList[i]
            if self.pebblesList[i] < 10:
                this_spot_str = " " + this_spot_str
            scores_str += this_spot_str
        return scores_str

    # switches whose turn it is
    def switch_turn(self):
        self.p1Turn = not self.p1Turn

################################################################################################
################################################################################################
################################################################################################


# Class that contains the methods that calculate the best moves for a given board
class AvalancheSolver(object):

    # constructor
    def __init__(self, board):
        self.board = board

    # Returns a copy of the game board
    def copy_board(self, board_to_copy):
        return AvalancheBoard(board_to_copy.pebblesList, board_to_copy.p1.copy_player(), board_to_copy.p2.copy_player(), board_to_copy.p1Turn)

    # Performs the moves of a given moveset on the given board
    def make_moves_on_moveset(self, move_list, board):
        prev_score = board.p1.score
        board.perform_move_set(move_list)
        return board.p1.score - prev_score

    # Perform a single move on a given board
    # returns the score for this turn, and whether or not the turn ended in the player's bank
    def make_move(self, index, board):
        prev_score = board.p1.score
        ended_in_bank = board.perform_move(index)
        return board.p1.score - prev_score, ended_in_bank

    # Recursive method that finds the best move for the player for a given board
    # returns the points gained from a moveset, and the moveset list
    def find_best_move(self, board, curr_val):
        index_options = self.get_list_of_non_zero_indexes(board)
        if len(index_options) == 0:
            # if no available moves
            return curr_val, []
        best_increase = -1
        best_move_list = [0]
        # loop through each available move
        for index in index_options:
            this_move_list = []
            board_copy = self.copy_board(board)
            make_move_results = self.make_move(index, board_copy)
            points_gained, ended_in_bank = make_move_results[0], make_move_results[1]
            if ended_in_bank:
                this_run_increase, this_move_list = self.find_best_move(board_copy, points_gained)
            else:
                this_run_increase = points_gained
            if this_run_increase > best_increase:
                best_increase = this_run_increase
                best_move_list = this_move_list.copy()
                best_move_list.insert(0, index)
        return best_increase + curr_val, best_move_list

    # get a list of the indexes that have pieces in them (and therefore are available to be played)
    def get_list_of_non_zero_indexes(self, board):
        non_zeros = []
        for i in range(0, 6, 1):
            if board.pebblesList[i] != 0:
                non_zeros.append(i)
        return non_zeros
