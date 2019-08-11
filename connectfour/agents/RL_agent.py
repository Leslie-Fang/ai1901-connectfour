from connectfour.agents.agent import Agent
import random

class RLAgent(Agent):
    def __init__(self, name):
        super().__init__(name)

    def DFS(self, id, scores, board, turn, mapping, search_deepth):
        # print("---------start new iteration-----------")
        if search_deepth <= 0:
            return
        # Here is first deepth's search
        if id is None:
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
                    # No win move, DFS to next search level, turn*(-1) to change player
                    self.DFS(i, scores, c_board, turn*(-1), mapping, search_deepth-1)
        # Generally search steps
        else:
            # Find all the possible moves
            cvalid_moves = board.valid_moves_v2()
            for i in range(len(cvalid_moves)):
                # Get the all the next board corresponding to the moves
                c_board = board.next_state_v2(cvalid_moves[i], mapping[turn])
                if c_board._check_rows() or c_board._check_columns() or c_board._check_diagonals():
                    # If find win moves, add the score in the scores
                    # turn 1: our player; tune -1: opponent player
                    scores[id] += turn * 100
                else:
                    # No win move, DFS to next search level, turn*(-1) to change player
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
            #print("--------cboard exits------------")
            return cboard
        #print("-----------Score------------")
        max_score = scores[0]
        best = []
        cvalid_moves = board.valid_moves_v2()
        # Find the moves with largest score
        for i in range(len(scores)):
            #print("move[{0}:{1}] score[{2}] is {3}".format(cvalid_moves[i][0], cvalid_moves[i][1], i, scores[i]))
            if scores[i] == max_score:
                best.append(i)
            elif scores[i] > max_score:
                max_score = scores[i]
                best = []
                best.append(i)
        # Random pick one move with largest score
        # id = random.choice(best)

        # Find the moves with longest link among the best
        max_connected_nums = []
        for move_candidate_id in best:
            max_connected = 0
            c_board = board.next_state_v2(cvalid_moves[move_candidate_id], mapping[1])
            temp = self.search_horizon(c_board)
            if temp > max_connected:
                max_connected = temp
            temp = self.search_vertical(c_board)
            if temp > max_connected:
                max_connected = temp
            temp = self.search_diagonals_from_leftrupper(c_board)
            if temp > max_connected:
                max_connected = temp
            temp = self.search_diagonals_from_rightrupper(c_board)
            if temp > max_connected:
                max_connected = temp
            max_connected_nums.append(max_connected)
        max_connected = 0
        best2 = []
        for i in range(len(max_connected_nums)):
            if max_connected_nums[i] == max_connected:
                #max_connected = max_connected_nums[i]
                best2.append(best[i])
            elif max_connected_nums[i] > max_connected:
                max_connected = max_connected_nums[i]
                best2 = []
                best2.append(best[i])

        # # Random pick one move with largest score
        # id = random.choice(best2)

        # Pick the one most close to the middle
        indexs_c = list(map(lambda x: abs(x - board.width / 2), best2))
        id = best2[indexs_c.index(min(indexs_c))]

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

    def search_horizon(self,board):
        last_move_row = board.last_move[0]
        last_move_column = board.last_move[1]
        cell_value = board.get_cell_value(last_move_row, last_move_column)
        connected_num = 1
        c_move_column = last_move_column
        while c_move_column+1 < board.width:
            c_move_column = c_move_column+1
            if board.get_cell_value(last_move_row, c_move_column) == cell_value:
                connected_num += 1
            else:
                break
        c_move_column = last_move_column
        while c_move_column-1 >= 0:
            c_move_column = c_move_column-1
            if board.get_cell_value(last_move_row, c_move_column) == cell_value:
                connected_num += 1
            else:
                break
        return connected_num

    def search_vertical(self,board):
        last_move_row = board.last_move[0]
        last_move_column = board.last_move[1]
        cell_value = board.get_cell_value(last_move_row,last_move_column)
        connected_num = 1
        c_move_row = last_move_row
        while c_move_row+1 < board.height:
            c_move_row = c_move_row + 1
            if board.get_cell_value(c_move_row,last_move_column) == cell_value:
                connected_num += 1
            else:
                break
        c_move_row = last_move_row
        while c_move_row - 1 >= 0:
            c_move_row = c_move_row - 1
            if board.get_cell_value(c_move_row,last_move_column) == cell_value:
                connected_num += 1
            else:
                break
        return connected_num

    def search_diagonals_from_leftrupper(self,board):
        last_move_row = board.last_move[0]
        last_move_column = board.last_move[1]
        cell_value = board.get_cell_value(last_move_row,last_move_column)
        connected_num = 1
        c_move_row = last_move_row
        c_move_column = last_move_column
        while c_move_row - 1 >=0 and c_move_column-1>=0:
            c_move_row -= 1
            c_move_column -= 1
            if board.get_cell_value(c_move_row,c_move_column) == cell_value:
                connected_num += 1
            else:
                break
        c_move_row = last_move_row
        c_move_column = last_move_column
        while c_move_row + 1 < board.height and c_move_column+1 < board.width:
            c_move_row += 1
            c_move_column += 1
            if board.get_cell_value(c_move_row,c_move_column) == cell_value:
                connected_num += 1
            else:
                break
        return connected_num


    def search_diagonals_from_rightrupper(self,board):
        last_move_row = board.last_move[0]
        last_move_column = board.last_move[1]
        cell_value = board.get_cell_value(last_move_row,last_move_column)
        connected_num = 1
        c_move_row = last_move_row
        c_move_column = last_move_column
        while c_move_row - 1 >=0 and c_move_column+1 < board.width:
            c_move_row -= 1
            c_move_column += 1
            if board.get_cell_value(c_move_row,c_move_column) == cell_value:
                connected_num += 1
            else:
                break
        c_move_row = last_move_row
        c_move_column = last_move_column
        while c_move_row + 1 < board.height and c_move_column - 1 >=0 :
            c_move_row += 1
            c_move_column -= 1
            if board.get_cell_value(c_move_row,c_move_column) == cell_value:
                connected_num += 1
            else:
                break
        return connected_num
