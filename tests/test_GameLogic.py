from GameLogic import *

from tests.utilsForTest import *


# Run with PyTest

class Test_getStraight:

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


class Test_findStrongest:

    class Test_StraightFlush:

        def test_baseCase_returnsCorrectly(self):
            three = Card(3, Suit.CLUBS)
            four = Card(4, Suit.CLUBS)
            five = Card(5, Suit.CLUBS)
            six = Card(6, Suit.CLUBS)
            seven = Card(7, Suit.CLUBS)
            nine = Card(9, Suit.DIAMONDS)
            jack = Card(11, Suit.SPADES)

            hand = Hand((six, five))
            board = Board((three, seven, jack, four, nine))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 8
            assert scored_hand.cards == [six, five]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [7, 6, 5, 4, 3]

        def test_multiplePossible_returnsCorrectly(self):
            three = Card(3, Suit.CLUBS)
            four = Card(4, Suit.CLUBS)
            five = Card(5, Suit.CLUBS)
            six = Card(6, Suit.CLUBS)
            seven = Card(7, Suit.CLUBS)
            eight = Card(8, Suit.CLUBS)
            jack = Card(11, Suit.SPADES)

            hand = Hand((six, five))
            board = Board((three, seven, jack, four, eight))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 8
            assert scored_hand.cards == [six, five]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [8, 7, 6, 5, 4]

    class Test_FourOfAKind:
        def test_withPair_returnsCorrectly(self):
            seven1 = Card(7, Suit.CLUBS)
            seven2 = Card(7, Suit.HEARTS)
            seven3 = Card(7, Suit.DIAMONDS)
            seven4 = Card(7, Suit.SPADES)
            ten1 = Card(10, Suit.SPADES)
            ten2 = Card(10, Suit.DIAMONDS)
            ace = Card(14, Suit.DIAMONDS)

            hand = Hand((seven1, seven2))
            board = Board((ten1, ten2, seven3, seven4, ace))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 7
            assert scored_hand.cards == [seven1, seven2]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [7, 7, 7, 7, 14]

        def test_baseCase_returnsCorrectly(self):
            nine1 = Card(9, Suit.CLUBS)
            nine2 = Card(9, Suit.HEARTS)
            nine3 = Card(9, Suit.DIAMONDS)
            nine4 = Card(9, Suit.SPADES)
            ten = Card(10, Suit.SPADES)
            four = Card(4, Suit.DIAMONDS)
            king = Card(13, Suit.DIAMONDS)

            hand = Hand((nine1, ten))
            board = Board((nine2, four, king, nine3, nine4))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 7
            assert scored_hand.cards == [nine1, ten]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [9, 9, 9, 9, 13]

    class Test_FullHouse:

        def test_twoTriplets_returnsCorrectly(self):
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
            assert scored_hand.cards == [king1, jack1]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [13, 13, 13, 11, 11]

        def test_TripletAnd2Pairs_returnsCorrectly(self):
            king1 = Card(13, Suit.CLUBS)
            king2 = Card(13, Suit.HEARTS)
            king3 = Card(13, Suit.DIAMONDS)
            ace1 = Card(14, Suit.CLUBS)
            ace2 = Card(14, Suit.SPADES)
            seven1 = Card(7, Suit.DIAMONDS)
            seven2 = Card(7, Suit.CLUBS)

            hand = Hand((king1, ace1))
            board = Board((seven1, seven2, ace2, king2, king3))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 6
            assert scored_hand.cards == [king1, ace1]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [13, 13, 13, 14, 14]

        def test_TripletAndPair_returnsCorrectly(self):
            six1 = Card(6, Suit.CLUBS)
            six2 = Card(6, Suit.HEARTS)
            six3 = Card(6, Suit.DIAMONDS)
            ten1 = Card(10, Suit.CLUBS)
            ten2 = Card(10, Suit.SPADES)
            other1 = Card(3, Suit.CLUBS)
            other2 = Card(9, Suit.SPADES)

            hand = Hand((six1, six2))
            board = Board((ten1, other1, other2, six3, ten2))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 6
            assert scored_hand.cards == [six1, six2]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [6, 6, 6, 10, 10]

    class Test_Flush:
        def test_baseCase_returnsCorrectly(self):
            seven = Card(7, Suit.SPADES)
            eight = Card(8, Suit.SPADES)
            nine = Card(9, Suit.SPADES)
            ten = Card(10, Suit.SPADES)
            four = Card(4, Suit.SPADES)
            three = Card(3, Suit.HEARTS)
            two = Card(2, Suit.DIAMONDS)

            hand = Hand((seven, eight))
            board = Board((nine, ten, four, three, two))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 5
            assert scored_hand.cards == [seven, eight]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [10, 9, 8, 7, 4]

        def test_possibleSet_returnsCorrectly(self):
            ace = Card(14, Suit.DIAMONDS)
            queen1 = Card(12, Suit.SPADES)
            queen2 = Card(12, Suit.DIAMONDS)
            queen3 = Card(12, Suit.HEARTS)
            ten = Card(10, Suit.DIAMONDS)
            four = Card(4, Suit.DIAMONDS)
            nine = Card(9, Suit.DIAMONDS)

            hand = Hand((ace, ten))
            board = Board((queen1, queen2, queen3, four, nine))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 5
            assert scored_hand.cards == [ace, ten]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [14, 12, 10, 9, 4]

        def test_possibleStraight_returnsCorrectly(self):
            ace = Card(14, Suit.SPADES)
            king = Card(13, Suit.SPADES)
            queen = Card(12, Suit.DIAMONDS)
            jack = Card(11, Suit.DIAMONDS)
            ten = Card(10, Suit.DIAMONDS)
            four = Card(4, Suit.DIAMONDS)
            nine = Card(9, Suit.DIAMONDS)

            hand = Hand((ace, ten))
            board = Board((king, queen, jack, four, nine))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 5
            assert scored_hand.cards == [ace, ten]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [12, 11, 10, 9, 4]

        def test_multiplePossible_returnsCorrectly(self):
            ace = Card(14, Suit.DIAMONDS)
            two = Card(2, Suit.DIAMONDS)
            queen = Card(12, Suit.DIAMONDS)
            six = Card(6, Suit.DIAMONDS)
            ten = Card(10, Suit.DIAMONDS)
            four = Card(4, Suit.DIAMONDS)
            nine = Card(9, Suit.DIAMONDS)

            hand = Hand((six, two))
            board = Board((ten, queen, ace, four, nine))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 5
            assert scored_hand.cards == [six, two]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [14, 12, 10, 9, 6]

    class Test_Straight:
        def test_baseCase_returnsCorrectly(self):
            five = Card(5, Suit.SPADES)
            six = Card(6, Suit.CLUBS)
            seven = Card(7, Suit.DIAMONDS)
            eight = Card(8, Suit.SPADES)
            nine = Card(9, Suit.HEARTS)
            two = Card(2, Suit.SPADES)
            three = Card(3, Suit.HEARTS)

            hand = Hand((five, six))
            board = Board((seven, nine, two, eight, three))

            scored_hand = find_strongest(hand, board)
            assert scored_hand.strength == 4
            assert scored_hand.cards == [five, six]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [9, 8, 7, 6, 5]

        def test_possibleSet_returnsCorrectly(self):
            seven = Card(7, Suit.SPADES)
            eight = Card(8, Suit.CLUBS)
            nine = Card(9, Suit.DIAMONDS)
            ten = Card(10, Suit.SPADES)
            jack1 = Card(11, Suit.HEARTS)
            jack2 = Card(11, Suit.SPADES)
            jack3 = Card(11, Suit.DIAMONDS)

            hand = Hand((seven, eight))
            board = Board((nine, jack3, jack2, jack1, ten))

            scored_hand = find_strongest(hand, board)
            assert scored_hand.strength == 4
            assert scored_hand.cards == [seven, eight]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [11, 10, 9, 8, 7]

        def test_almostFlush_returnsCorrectly(self):
            seven = Card(7, Suit.SPADES)
            eight = Card(8, Suit.SPADES)
            nine = Card(9, Suit.SPADES)
            ten = Card(10, Suit.SPADES)
            jack = Card(11, Suit.HEARTS)
            three = Card(3, Suit.HEARTS)
            two = Card(2, Suit.DIAMONDS)

            hand = Hand((seven, eight))
            board = Board((nine, jack, three, two, ten))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 4
            assert scored_hand.cards == [seven, eight]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [11, 10, 9, 8, 7]

        def test_multiplePossible_returnsCorrectly(self):
            hand = Hand((king_c, nine_c))
            board = Board((ten_d, queen_h, jack_d, eight_c, ace_s))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 4
            assert scored_hand.cards == [king_c, nine_c]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [14, 13, 12, 11, 10]

    class Test_ThreeOfAKind:
        def test_baseCase_returnsCorrectly(self):
            three1 = Card(3, Suit.CLUBS)
            three2 = Card(3, Suit.HEARTS)
            three3 = Card(3, Suit.DIAMONDS)
            ace = Card(14, Suit.CLUBS)
            ten = Card(10, Suit.SPADES)
            seven = Card(7, Suit.CLUBS)
            nine = Card(9, Suit.SPADES)

            hand = Hand((three1, ace))
            board = Board((three2, three3, ten, seven, nine))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 3
            assert scored_hand.cards == [three1, ace]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [3, 3, 3, 14, 10]

    class Test_TwoPair:
        def test_baseCase_returnsCorrectly(self):
            seven1 = Card(7, Suit.CLUBS)
            seven2 = Card(7, Suit.HEARTS)
            ten1 = Card(10, Suit.CLUBS)
            ten2 = Card(10, Suit.SPADES)
            four = Card(4, Suit.CLUBS)
            nine = Card(9, Suit.SPADES)
            jack = Card(11, Suit.SPADES)

            hand = Hand((four, jack))
            board = Board((seven2, nine, ten1, seven1, ten2))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 2
            assert scored_hand.cards == [four, jack]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [10, 10, 7, 7, 11]

        def test_threePairs_returnsCorrectly(self):
            seven1 = Card(7, Suit.CLUBS)
            seven2 = Card(7, Suit.HEARTS)
            ten1 = Card(10, Suit.CLUBS)
            ten2 = Card(10, Suit.SPADES)
            four1 = Card(4, Suit.CLUBS)
            four2 = Card(4, Suit.SPADES)
            jack = Card(11, Suit.SPADES)

            hand = Hand((four1, jack))
            board = Board((seven2, four2, ten1, seven1, ten2))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 2
            assert scored_hand.cards == [four1, jack]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [10, 10, 7, 7, 11]

    class Test_Pair:
        def test_Pair_baseCase_returnsCorrectly(self):
            seven1 = Card(7, Suit.CLUBS)
            seven2 = Card(7, Suit.HEARTS)
            ace = Card(14, Suit.CLUBS)
            ten = Card(10, Suit.SPADES)
            four = Card(4, Suit.CLUBS)
            nine = Card(9, Suit.SPADES)
            jack = Card(11, Suit.SPADES)

            hand = Hand((four, jack))
            board = Board((seven2, nine, ten, seven1, ace))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 1
            assert scored_hand.cards == [four, jack]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [7, 7, 14, 11, 10]

    class Test_HighCard:
        def test_highCard_baseCase_returnsCorrectly(self):
            two = Card(2, Suit.CLUBS)
            four = Card(4, Suit.DIAMONDS)
            six = Card(6, Suit.HEARTS)
            eight = Card(8, Suit.HEARTS)
            ten = Card(10, Suit.SPADES)
            jack = Card(11, Suit.HEARTS)
            king = Card(13, Suit.CLUBS)

            hand = Hand((six, jack))
            board = Board((ten, two, king, four, eight))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 0
            assert scored_hand.cards == [six, jack]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [13, 11, 10, 8, 6]


class Test_get_scoring_order:

    def test_baseCase_returnsCorrectly(self):
        top_hand = Hand((king_c, ten_c))
        second_hand = Hand((nine_d, nine_h))
        bottom_hand = Hand((nine_s, three_h))

        # board = Board((nine_c, four_c, ace_c, two_d, seven_h))

        top_hand.strength = 5  # flush
        second_hand.strength = 3  # three of a kind
        bottom_hand.strength = 1  # pair

        top_hand.best_5 = [ace_c, king_c, ten_c, nine_c, four_c]
        second_hand.best_5 = [nine_c, nine_d, nine_h, ace_c, seven_h]
        bottom_hand.best_5 = [nine_c, nine_s, ace_c, seven_h, four_c]

        sorted_hands = get_scoring_order(bottom_hand, top_hand, second_hand)

        assert sorted_hands == [[top_hand], [second_hand], [bottom_hand]]

    def test_withTie_returnsCorrectly(self):
        top_hand = Hand()
        second_hand = Hand()
        tied_second_hand = Hand()
        bottom_hand = Hand()

        top_hand.strength = 3  # 3 of a kind
        second_hand.strength = 2  # two pair
        tied_second_hand.strength = 2  # two pair, same as above
        bottom_hand.strength = 2  # two pair, worse kicker

        top_hand.best_5 = [seven_h, seven_c, seven_d, ace_c, king_h]
        second_hand.best_5 = [ace_c, ace_d, seven_h, seven_c, nine_d]
        tied_second_hand.best_5 = [ace_c, ace_h, seven_h, seven_c, nine_h]
        bottom_hand.best_5 = [ace_c, ace_s, seven_h, seven_c, four_c]

        sorted_hands = get_scoring_order(bottom_hand, top_hand, tied_second_hand, second_hand)

        assert sorted_hands == [[top_hand], [second_hand, tied_second_hand], [bottom_hand]]
