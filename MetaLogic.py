from collections import defaultdict
from itertools import combinations
from typing import List, Optional

from GameLogic import *
from PokerObjects import *


def get_winner(hands: List[Hand], board: Board) -> Optional[Hand]:
    """Takes in a hands and complete board, returns winning hand or none if tied."""
    if len(board.cards) != 5:
        raise ValueError(
            f"Board is the wrong length: expected length is 5, but given {len(board.cards)}.\n Board == {board}"
        )

    scored_hands = []
    for hand in hands:
        scored_hands.append(find_strongest(hand=hand, board=board))
    scoring_order = get_scoring_order(*scored_hands)
    if len(scoring_order[0]) == 1:
        return scoring_order[0][0]
    else:
        return None  # currently ignores that 2 hands can tie in 3+ hand set. All ties treated as the same.


def get_outs(hands: List[Hand], board: Board):

    # TODO: Fiddle with this to allow it to take in empty hands and get odds for one to win
    deck = [c for c in Deck().cards if c not in [c for hand in hands for c in hand.cards] and c not in board.cards]
    win_dict = defaultdict(int)

    for board_combination in combinations(deck, 5-len(board.cards)):
        current_board = Board(*(board.cards + list(board_combination)))

        if (hand := get_winner(hands, current_board)) is not None:
            win_dict[hand] += 1
        else:
            win_dict["Tie"] += 1

    return win_dict
