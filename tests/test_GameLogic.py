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

    def test_tooFewCards_returnsNone(self):
        sq = Card(12, Suit.SPADES)
        hj = Card(11, Suit.HEARTS)
        h10 = Card(10, Suit.HEARTS)
        c9 = Card(9, Suit.CLUBS)

        cards = [sq, h10, hj, c9]
        returned = get_straight(cards)

        assert returned is None

    def test_multipleStraights_returnsHighest(self):
        queen = Card(12, Suit.CLUBS)
        jack = Card(11, Suit.HEARTS)
        ten = Card(10, Suit.SPADES)
        nine = Card(9, Suit.DIAMONDS)
        eight = Card(8, Suit.CLUBS)
        seven = Card(7, Suit.HEARTS)

        cards = [jack, ten, nine, queen, seven, eight]
        returned = get_straight(cards)

        assert returned == [queen, jack, ten, nine, eight]

    def test_noStraight_returnsNone(self):
        queen = Card(12, Suit.CLUBS)
        jack = Card(11, Suit.HEARTS)
        four = Card(4, Suit.SPADES)
        nine = Card(9, Suit.DIAMONDS)
        eight = Card(8, Suit.CLUBS)
        seven = Card(7, Suit.HEARTS)

        cards = [jack, four, nine, queen, seven, eight]
        returned = get_straight(cards)

        assert returned is None

class Test_find_strongest:

    def test_FullHouse_twoTriplets_returnsCorrectly(self):
        king1 = Card(13, Suit.CLUBS)
        king2 = Card(13, Suit.HEARTS)
        king3 = Card(13, Suit.DIAMONDS)
        jack1 = Card(11, Suit.CLUBS)
        jack2 = Card(11, Suit.SPADES)
        jack3 = Card(11, Suit.DIAMONDS)
        other_card = Card(5, Suit.DIAMONDS)

        hand = Hand((king1, jack1))
        board = Board((king2, king3, jack2, jack3, other_card))

        scored_hand = find_strongest(hand, board)

        assert scored_hand.strength == 6
        assert len(scored_hand.best_5) == 5
        assert len(scored_hand.cards) == 2
        assert Counter([c.value for c in scored_hand.best_5]) == Counter([13, 13, 13, 11, 11])
