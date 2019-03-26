from connectfour.agents.agent import Agent
import random

class state(object):
    def __init__(
        self,
        board=None,
    ):
        self.board = board

class RLAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def DFS(self, id, scores, board, turn, mapping, search_deepth):
        print("---------start new iteration-----------")
        if search_deepth <= 0:
            return
        if id is None:
            # Here is first deepth's search
            # Find all the possible moves
            cvalid_moves = board.valid_moves_v2()
            for i in range(len(cvalid_moves)):
                scores.append(0)
                # Get the all the next board corresponding to the moves
                c_board = board.next_state_v2(cvalid_moves[i], mapping[turn])
                if c_board._check_rows() or c_board._check_columns() or c_board._check_diagonals():
                    # If the first move makes it win, just move it.
                    return c_board
                else:
                    # No win move, DFS to next search level
                    self.DFS(i, scores, c_board, turn*(-1), mapping, search_deepth-1)
        else:
            # Generally search steps
            # Find all the possible moves
            cvalid_moves = board.valid_moves_v2()
            for i in range(len(cvalid_moves)):
                print(len(cvalid_moves))
                # Get the all the next board corresponding to the moves
                c_board = board.next_state_v2(cvalid_moves[i], mapping[turn])
                if c_board._check_rows() or c_board._check_columns() or c_board._check_diagonals():
                    # If find win moves, add the score in the scores
                    scores[id] += turn * 100
                else:
                    self.DFS(id, scores, c_board, turn * (-1), mapping, search_deepth-1)
            return None

    def find_best_move(self, board, search_deepth):
        if self.id == 1:
            mapping = {1: 1, -1: 2}
        else:
            mapping = {1: 2, -1: 1}
        scores = []  # scores of every possible move
        turn = 1
        cboard = self.DFS(None, scores, board, turn, mapping, search_deepth)
        if cboard:
            print("--------cboard exits------------")
            return cboard
        print("-----------Score------------")
        max_score = scores[0]
        best = []
        for i in range(len(scores)):
            print("score[{0}] is {1}".format(i, scores[i]))
            if scores[i] == max_score:
                best.append(i)
            elif scores[i] > max_score:
                max_score = scores[i]
                best = []
                best.append(i)
        id = random.choice(best)
        cvalid_moves = board.valid_moves_v2()
        return board.next_state_v2(cvalid_moves[id], mapping[1])

    def _find_move_from_new_board_state(self, old, new):
        """
        Making a move in Connect Four makes exactly one change to the board.
        Searching through all x,y positions for a difference between the old and
        new board will tell us exactly where a move was made.
        """
        for x in range(len(old)):
            for y in range(len(old[0])):
                if old[x][y] != new[x][y]:
                    return x, y
        return -1, -1

    def get_move(self, board):
        """
        Args:
            board: An instance of `Board` that is the current state of the board.

        Returns:
            A tuple of two integers, (row, col)
        """

        """
        These are the variables and functions for board objects which may be helpful when creating your Agent.
        Look into board.py for more information/descriptions of each, or to look for any other definitions which may help you.

        Board Variables:
            board.width 
            board.height
            board.last_move
            board.num_to_connect
            board.winning_zones
            board.score_array 
            board.current_player_score

        Board Functions:
            get_cell_value(row, col)
            try_move(col)
            valid_move(row, col)
            valid_moves()
            terminal(self)
            legal_moves()
            next_state(turn)
            winner()
        """
        best_move = self.find_best_move(board, 4)
        return self._find_move_from_new_board_state(board.board, best_move.board)

    def evaluateBoardState(self, board, player):
        """
        Your evaluation function should look at the current state and return a score for it.
        As an example, the random agent provided works as follows:
            If the opponent has won this game, return -1.
            If we have won the game, return 1.
            If neither of the players has won, return a random number.
        """

        return 0
