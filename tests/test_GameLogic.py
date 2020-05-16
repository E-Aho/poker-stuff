from GameLogic import *


class Test_get_straight:

    def test_normalCase_returnsStraight(self):
        s2 = Card(2, Suit.SPADES)
        h3 = Card(3, Suit.HEARTS)
        d4 = Card(4, Suit.DIAMONDS)
        d5 = Card(5, Suit.DIAMONDS)
        s6 = Card(6, Suit.SPADES)
        ck = Card(13, Suit.CLUBS)

        cards = [s2, h3, s6, d5, d4, ck]

        returned_val = get_straight(cards)

        assert returned_val == [s6, d5, d4, h3, s2]

    def test_withAceLow_returnsStraight(self):
        s2 = Card(2, Suit.SPADES)
        h3 = Card(3, Suit.HEARTS)
        d4 = Card(4, Suit.DIAMONDS)
        d5 = Card(5, Suit.DIAMONDS)
        sa = Card(14, Suit.SPADES)
        ck = Card(13, Suit.CLUBS)

        cards = [s2, h3, d4, d5, sa, ck]

        returned_val = get_straight(cards)

        assert returned_val == [d5, d4, h3, s2, sa]

    def test_withAceHigh_returnsStraight(self):
        sa = Card(14, Suit.SPADES)
        dk = Card(13, Suit.DIAMONDS)
        sq = Card(12, Suit.SPADES)
        hj = Card(11, Suit.HEARTS)
        h10 = Card(10, Suit.HEARTS)
        c4 = Card(4, Suit.CLUBS)
        c8 = Card(8, Suit.CLUBS)

        cards = [c8, sa, sq, hj, dk, c4, h10]

        returned = get_straight(cards)

        assert returned == [sa, dk, sq, hj, h10]

    def test_withDuplicates_returnsStraight(self):
        dk = Card(13, Suit.DIAMONDS)
        hk = Card(13, Suit.HEARTS)
        sq = Card(12, Suit.SPADES)
        hj = Card(11, Suit.HEARTS)
        h10 = Card(10, Suit.HEARTS)
        c9 = Card(9, Suit.CLUBS)
        c4 = Card(4, Suit.CLUBS)
        c8 = Card(8, Suit.CLUBS)

        cards = [c8, hk, sq, hj, dk, c4, h10, c9]

        returned = get_straight(cards)

        straight1 = [hk, sq, hj, h10, c9]
        straight2 = [dk, sq, hj, h10, c9]

        assert returned == straight1 or straight2

