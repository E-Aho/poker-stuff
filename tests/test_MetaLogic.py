from MetaLogic import *
from PokerObjects import *

from tests.utilsForTest import *

# Run with PyTest


def test_get_odds():
    hand_1 = Hand(ace_s, ace_h)
    hand_2 = Hand(two_c, two_d)
    empty_board = Board((queen_c, seven_d, nine_c, king_s))

    win_dict = get_odds([hand_1, hand_2], empty_board)
    assert win_dict == {"Tie"}
    # TODO: odds not calculating right, not considering cards missing from hand correctly