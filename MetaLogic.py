from collections import defaultdict
from itertools import permutations, combinations
from typing import List

from GameLogic import *
from PokerObjects import *


def get_outs(hands: List[Hand], board: Board):

    # TODO: Fiddle with this to allow it to take in empty hands and get odds for one to win
    deck = [c for c in Deck().cards if c not in [c for hand in hands for c in hand.cards] and c not in board.cards]
    win_dict = defaultdict(int)

    for board_combination in combinations(deck, 5-len(board.cards)):
        current_board = Board(*(board.cards + list(board_combination)))
        scored_hands = []
        for hand in hands:
            scored_hands.append(find_strongest(hand=hand, board=current_board))
        scoring_order = get_scoring_order(*scored_hands)
        if len(scoring_order[0]) == 1:
            win_dict[scoring_order[0][0]] += 1
        elif len(scoring_order[0]) > 1:  # Consider changing if more than 2 hands used here
            win_dict["Tie"] += 1
    return win_dict
