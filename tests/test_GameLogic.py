from itertools import permutations

from GameLogic import *

from tests.utilsForTest import *

# Run with PyTest


class Test_getStraight:

    def test_normalCase_returnsStraight(self):
        cards = [two_s, three_h, six_d, five_d, four_c, king_c]

        assert get_straight(cards) == [six_d, five_d, four_c, three_h, two_s]

    def test_withAceLow_returnsStraight(self):
        cards = [two_s, three_h, four_h, five_d, ace_c, king_c]

        assert get_straight(cards) == [five_d, four_h, three_h, two_s, ace_c]

    def test_withAceHigh_returnsStraight(self):
        cards = [eight_c, ace_s, queen_s, jack_h, king_d, four_d, ten_h]

        assert get_straight(cards) == [ace_s, king_d, queen_s, jack_h, ten_h]

    def test_withDuplicates_returnsStraight(self):
        cards = [eight_s, king_h, queen_d, jack_c, king_d, four_d, ten_d, nine_c]

        straight1 = [king_h, queen_d, jack_c, ten_d, nine_c]
        straight2 = [king_d, queen_d, jack_c, ten_d, nine_c]

        assert get_straight(cards) == straight1 or straight2

    def test_tooFewCards_returnsNone(self):
        cards = [queen_c, ten_d, jack_d, nine_c]

        assert get_straight(cards) is None

    def test_multipleStraights_returnsHighest(self):
        cards = [jack_d, ten_c, nine_s, queen_h, seven_s, eight_d]

        assert get_straight(cards) == [queen_h, jack_d, ten_c, nine_s, eight_d]

    def test_noStraight_returnsNone(self):
        cards = [jack_s, four_d, nine_c, queen_d, seven_c, eight_d]

        assert get_straight(cards) is None


class Test_findStrongest:

    class Test_StraightFlush:

        def test_baseCase_returnsCorrectly(self):
            hand = Hand(six_c, five_c)
            board = Board((three_c, seven_c, jack_h, four_c, nine_d))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 8
            assert scored_hand.cards == [six_c, five_c]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [7, 6, 5, 4, 3]

        def test_multiplePossible_returnsCorrectly(self):
            hand = Hand(six_c, five_c)
            board = Board((three_c, seven_c, jack_d, four_c, eight_c))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 8
            assert scored_hand.cards == [six_c, five_c]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [8, 7, 6, 5, 4]

    class Test_FourOfAKind:
        def test_withPair_returnsCorrectly(self):
            hand = Hand(seven_c, seven_h)
            board = Board((ten_s, ten_d, seven_d, seven_s, ace_d))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 7
            assert scored_hand.cards == [seven_c, seven_h]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [7, 7, 7, 7, 14]

        def test_baseCase_returnsCorrectly(self):
            hand = Hand(nine_c, ten_d)
            board = Board((nine_h, four_c, king_h, nine_d, nine_s))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 7
            assert scored_hand.cards == [nine_c, ten_d]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [9, 9, 9, 9, 13]

    class Test_FullHouse:

        def test_twoTriplets_returnsCorrectly(self):
            hand = Hand(king_c, jack_c)
            board = Board((king_h, king_d, jack_s, jack_d, five_d))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 6
            assert scored_hand.cards == [king_c, jack_c]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [13, 13, 13, 11, 11]

        def test_TripletAnd2Pairs_returnsCorrectly(self):
            hand = Hand(king_c, ace_c)
            board = Board((seven_d, seven_c, ace_s, king_h, king_d))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 6
            assert scored_hand.cards == [king_c, ace_c]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [13, 13, 13, 14, 14]

        def test_TripletAndPair_returnsCorrectly(self):
            hand = Hand(six_c, six_h)
            board = Board((ten_c, three_d, king_d, six_d, ten_s))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 6
            assert scored_hand.cards == [six_c, six_h]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [6, 6, 6, 10, 10]

    class Test_Flush:
        def test_baseCase_returnsCorrectly(self):
            hand = Hand(seven_s, eight_s)
            board = Board((nine_s, ten_s, four_s, three_h, two_d))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 5
            assert scored_hand.cards == [seven_s, eight_s]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [10, 9, 8, 7, 4]

        def test_possibleSet_returnsCorrectly(self):
            hand = Hand(ace_d, ten_d)
            board = Board((queen_s, queen_d, queen_h, four_d, nine_d))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 5
            assert scored_hand.cards == [ace_d, ten_d]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [14, 12, 10, 9, 4]

        def test_possibleStraight_returnsCorrectly(self):
            hand = Hand(ace_s, ten_d)
            board = Board((king_s, queen_d, jack_d, four_d, seven_d))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 5
            assert scored_hand.cards == [ace_s, ten_d]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [12, 11, 10, 7, 4]

        def test_multiplePossible_returnsCorrectly(self):
            hand = Hand(six_d, two_d)
            board = Board((ten_d, queen_d, ace_d, four_d, nine_d))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 5
            assert scored_hand.cards == [six_d, two_d]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [14, 12, 10, 9, 6]

    class Test_Straight:
        def test_baseCase_returnsCorrectly(self):
            hand = Hand(five_s, six_c)
            board = Board((seven_d, nine_h, two_s, eight_s, three_h))

            scored_hand = find_strongest(hand, board)
            assert scored_hand.strength == 4
            assert scored_hand.cards == [five_s, six_c]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [9, 8, 7, 6, 5]

        def test_possibleSet_returnsCorrectly(self):
            hand = Hand(seven_s, eight_c)
            board = Board((nine_d, jack_d, jack_s, jack_h, ten_s))

            scored_hand = find_strongest(hand, board)
            assert scored_hand.strength == 4
            assert scored_hand.cards == [seven_s, eight_c]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [11, 10, 9, 8, 7]

        def test_almostFlush_returnsCorrectly(self):
            hand = Hand(seven_s, eight_s)
            board = Board((nine_s, jack_h, three_h, two_d, ten_s))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 4
            assert scored_hand.cards == [seven_s, eight_s]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [11, 10, 9, 8, 7]

        def test_multiplePossible_returnsCorrectly(self):
            hand = Hand(king_c, nine_c)
            board = Board((ten_d, queen_h, jack_d, eight_c, ace_s))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 4
            assert scored_hand.cards == [king_c, nine_c]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [14, 13, 12, 11, 10]

    class Test_ThreeOfAKind:
        def test_baseCase_returnsCorrectly(self):
            hand = Hand(three_c, ace_c)
            board = Board((three_h, three_d, ten_s, seven_c, nine_s))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 3
            assert scored_hand.cards == [three_c, ace_c]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [3, 3, 3, 14, 10]

    class Test_TwoPair:
        def test_baseCase_returnsCorrectly(self):
            hand = Hand(four_c, jack_s)
            board = Board((seven_h, nine_s, ten_c, seven_c, ten_s))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 2
            assert scored_hand.cards == [four_c, jack_s]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [10, 10, 7, 7, 11]

        def test_threePairs_returnsCorrectly(self):
            hand = Hand(four_c, jack_s)
            board = Board((seven_h, four_s, ten_c, seven_c, ten_s))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 2
            assert scored_hand.cards == [four_c, jack_s]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [10, 10, 7, 7, 11]

    class Test_Pair:
        def test_Pair_baseCase_returnsCorrectly(self):
            hand = Hand(four_c, jack_s)
            board = Board((seven_h, nine_s, ten_s, seven_c, ace_c))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 1
            assert scored_hand.cards == [four_c, jack_s]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [7, 7, 14, 11, 10]

    class Test_HighCard:
        def test_highCard_baseCase_returnsCorrectly(self):
            hand = Hand(six_h, jack_h)
            board = Board((ten_s, two_c, king_c, four_d, eight_h))

            scored_hand = find_strongest(hand, board)

            assert scored_hand.strength == 0
            assert scored_hand.cards == [six_h, jack_h]
            assert len(scored_hand.best_5) == 5
            assert [c.value for c in scored_hand.best_5] == [13, 11, 10, 8, 6]


class Test_get_scoring_order:

    def test_baseCase_returnsCorrectly(self):
        top_hand = Hand(king_c, ten_c)
        second_hand = Hand(nine_d, nine_h)
        bottom_hand = Hand(nine_s, three_h)

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

        first_permutation = [[top_hand], [second_hand, tied_second_hand], [bottom_hand]]
        second_permutation = [[top_hand], [tied_second_hand, second_hand], [bottom_hand]]

        assert sorted_hands == first_permutation or second_permutation

    def test_with3WayTie_returnsCorrectly(self):
        tied_hand_1 = Hand().withStrength(4)  # straight
        tied_hand_2 = Hand().withStrength(4)  # straight
        tied_hand_3 = Hand().withStrength(4)  # straight
        bottom_hand = Hand().withStrength(3)  # 3 of a kind

        tied_hand_1.best_5 = [ten_c, nine_d, eight_c, seven_c, six_d]
        tied_hand_2.best_5 = [ten_c, nine_s, eight_c, seven_c, six_h]
        tied_hand_3.best_5 = [ten_c, nine_h, eight_c, seven_c, six_s]
        bottom_hand.best_5 = [ten_c, ten_d, ten_s, ace_c, eight_c]

        sorted_hands = get_scoring_order(tied_hand_1, bottom_hand, tied_hand_2, tied_hand_3)

        expected_outputs = [[list(p), [bottom_hand]] for p in list(permutations([tied_hand_1, tied_hand_2, tied_hand_3]))]

        assert sorted_hands in expected_outputs

    def test_withMultipleTies_returnsCorrectly(self):

        tie_a1 = Hand().withStrength(6)  # full house
        tie_a2 = Hand().withStrength(6)  # full house
        tie_b1 = Hand().withStrength(4)  # straight
        tie_b2 = Hand().withStrength(4)  # straight
        tie_b3 = Hand().withStrength(4)  # straight

        tie_a1.best_5 = [two_s, two_d, two_c, three_c, three_d]
        tie_a2.best_5 = [two_c, two_d, two_h, three_c, three_d]
        tie_b1.best_5 = [six_c, five_d, four_h, three_d, two_c]
        tie_b2.best_5 = [six_d, five_h, four_h, three_d, two_c]
        tie_b3.best_5 = [six_h, five_s, four_h, three_d, two_c]

        ties_a = permutations([tie_a1, tie_a2])
        ties_b = permutations([tie_b3, tie_b2, tie_b1])

        sorted_hands = get_scoring_order(tie_a1, tie_a2, tie_b1, tie_b2, tie_b3)

        expected_outputs = [[list(perm_a), list(perm_b)] for perm_a in ties_a for perm_b in ties_b]
        assert sorted_hands in expected_outputs


class Test_Integration:

    def test_givenHands_evaluateToGiveWinner(self):

        player_1 = Hand(two_s, two_d)
        player_2 = Hand(three_h, four_d)

        board = Board((two_c, five_c, six_d, king_c, nine_h))

        player_1 = find_strongest(player_1, board)
        player_2 = find_strongest(player_2, board)

        assert get_scoring_order(player_2, player_1) == [[player_2], [player_1]]

