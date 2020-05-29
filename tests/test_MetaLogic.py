from MetaLogic import *
from PokerObjects import *

from tests.utilsForTest import *


# Run with PyTest


class Test_get_outs:
    def test_oneCardLeft_withTwoPairs_returnsCorrectly(self):
        hand_1 = Hand(ace_s, ace_h)
        hand_2 = Hand(two_c, two_d)
        board = Board(queen_c, seven_d, nine_c, king_s)

        win_dict = get_outs([hand_1, hand_2], board)

        assert win_dict["Tie"] == 0
        assert win_dict[hand_1] == 42
        assert win_dict[hand_2] == 2

    def test_afterFlop_flushVsStraight_returnsCorrectly(self):
        flush_hand = Hand(seven_s, two_s)
        straight_hand = Hand(seven_c, six_d)
        board = Board(five_s, four_s, king_d)

        win_dict = get_outs([flush_hand, straight_hand], board)
        assert win_dict["Tie"] == 141
        assert win_dict[flush_hand] == 438
        assert win_dict[straight_hand] == 411

    def test_withThreeHands_afterFlop_returnsCorrectly(self):
        top_hand = Hand(ace_h, king_h)
        mid_hand = Hand(queen_h, jack_h)
        low_hand = Hand(ten_h, nine_h)
        board = Board(king_s, ten_d, six_s)

        win_dict = get_outs([top_hand, mid_hand, low_hand], board)
        assert win_dict["Tie"] == 0
        assert win_dict[top_hand] == 586
        assert win_dict[mid_hand] == 225
        assert win_dict[low_hand] == 92

    def test_oneCardLeft_withTwoPairs_returnsCorrectly(self):
        hand_1 = Hand(ace_s, ace_h)
        hand_2 = Hand(two_c, two_d)
        board = Board(queen_c, seven_d, nine_c, king_s)

        win_dict = get_outs_multithreaded([hand_1, hand_2], board)

        assert win_dict["Tie"] == 0
        assert win_dict[hand_1] == 42
        assert win_dict[hand_2] == 2