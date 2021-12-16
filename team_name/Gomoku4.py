#!/usr/bin/env python
#/usr/local/bin/python3
# Set the path to your python3 above

from gtp_connection import GtpConnection
from board_util import GoBoardUtil, EMPTY
from simple_board import SimpleGoBoard
from mcts import MCTS

import random
import numpy as np

def undo(board,move):
    board.board[move]=EMPTY
    board.current_player=GoBoardUtil.opponent(board.current_player)

def play_move(board, move, color):
    board.play_move_gomoku(move, color)

def game_result(board):
    game_end, winner = board.check_game_end_gomoku()
    moves = board.get_empty_points()
    board_full = (len(moves) == 0)
    if game_end:
        #return 1 if winner == board.current_player else -1
        return winner
    if board_full:
        return 'draw'
    return None

class GomokuSimulationPlayer(object):
    """
    For each move do `n_simualtions_per_move` playouts,
    then select the one with best win-rate.
    playout could be either random or rule_based (i.e., uses pre-defined patterns)
    """
    def __init__(
        self,
        num_sim,
        sim_rule,
        move_filter,
        in_tree_knowledge,
        size=7,
        limit=100,
        exploration=0.4,
    ):
        """
        Player that selects a move based on MCTS from the set of legal moves
        """
        self.name = "Gomoku4"
        self.version = "1.0"
        self.komi = 6.5
        self.MCTS = MCTS()
        self.num_simulation = num_sim
        self.limit = limit
        self.exploration = exploration
        self.simulation_policy = sim_rule
        self.use_pattern = True
        self.check_selfatari = move_filter
        self.in_tree_knowledge = in_tree_knowledge
        self.parent = None


    def reset(self):
        self.MCTS = MCTS()

    def update(self, move):
        self.parent = self.MCTS._root
        self.MCTS.update_with_move(move)

    # def set_playout_policy(self, playout_policy='random'):
    #     assert(playout_policy in ['random', 'rule_based'])
    #     self.playout_policy=playout_policy

    # def _random_moves(self, board, color_to_play):
    #     return GoBoardUtil.generate_legal_moves_gomoku(board)

    # def policy_moves(self, board, color_to_play):

    #     assert(isinstance(board, SimpleGoBoard))
    #     ret=board.get_pattern_moves()
    #     movetype_id, moves=ret
    #     return self.pattern_list[movetype_id], moves

    # def _do_playout(self, board, color_to_play):
    #     res=game_result(board)
    #     simulation_moves=[]
    #     while(res is None):
    #         _ , candidate_moves = self.policy_moves(board, board.current_player)
    #         playout_move=random.choice(candidate_moves)
    #         play_move(board, playout_move, board.current_player)
    #         simulation_moves.append(playout_move)
    #         res=game_result(board)
    #     for m in simulation_moves[::-1]:
    #         undo(board, m)
    #     if res == color_to_play:
    #         return 1.0
    #     elif res == 'draw':
    #         return 0.0
    #     else:
    #         assert(res == GoBoardUtil.opponent(color_to_play))
    #         return -1.0

    def get_move(self, board, toplay):
        move = self.MCTS.get_move(
            board,
            toplay,
            komi=self.komi,
            limit=self.limit,
            check_selfatari=self.check_selfatari,
            use_pattern=self.use_pattern,
            num_simulation=self.num_simulation,
            exploration=self.exploration,
            simulation_policy=self.simulation_policy,
            in_tree_knowledge=self.in_tree_knowledge,
        )
        self.update(move)
        return move

    # def point_weight(self, point, color, board):
    #     check_list = [-1, 1, -board.NS, board.NS, -board.NS-1, - board.NS + 1, + board.NS - 1, + board.NS + 1]
    #     weight = 0
    #     for direction in check_list:
    #         a = 1
    #         b = 1
    #         temp_weight = 0
    #         for i in range(4):
    #             next = point + direction*(i+1)
    #             if next >= len(board.board):
    #                 break
    #             if board.get_color(next) == color:
    #                 temp_weight += a
    #                 a *= 3
    #                 if i == b-1:
    #                     b += 1
    #         temp_weight *= b
    #         weight += temp_weight
    #     return weight

    # def sort_value_moves(self,value_moves,toplay, board):
    #     move_weight = dict()
    #     for move in value_moves:
    #         weight = self.point_weight(move,toplay, board)
    #         move_weight[move] = weight


    #     sorted_moves = sorted(move_weight.keys(), key=lambda d: move_weight[d], reverse = True)
    #     return sorted_moves














def run():
    """
    start the gtp connection and wait for commands.
    """
    board = SimpleGoBoard(7)
    con = GtpConnection(GomokuSimulationPlayer(), board)
    con.start_connection()

if __name__=='__main__':
    run()
