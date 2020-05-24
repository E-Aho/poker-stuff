from PokerObjects import *

from tests.utilsForTest import *

# Run with PyTest


class Test_Card:

    def test_Card_equals_whenEqual(self):
        card_a = Card(5, Suit.DIAMONDS)
        card_b = Card(5, Suit.DIAMONDS)

        assert card_a == card_b

    def test_Card_equals_whenNotEqual(self):
        card_a = Card(5, Suit.DIAMONDS)
        card_b = Card(5, Suit.HEARTS)
        card_c = Card(7, Suit.DIAMONDS)
        card_d = Card(14, Suit.SPADES)

        assert card_a != card_b
        assert card_a != card_c
        assert card_a != card_d
        assert card_b != card_c
        assert card_b != card_d


class Test_Card_Collection:

    def test_gt_HighCard_whenGreater(self):
        bigger_collection = Card_Collection(king_c, queen_c, ten_d, four_c, three_d)
        smaller_collection = Card_Collection(king_c, jack_c, ten_d, nine_c, three_d)

        assert bigger_collection > smaller_collection

    def test_gt_set_whenGreater(self):
        bigger_collection = Card_Collection(seven_d, seven_c, ten_d, four_c, three_d)
        smaller_collection = Card_Collection(four_c, four_d, ten_d, nine_c, three_d)

        assert bigger_collection > smaller_collection

    def test_gt_sets_whenSmaller(self):
        bigger_collection = Card_Collection(seven_d, seven_c, ten_d, four_c, three_d)
        smaller_collection = Card_Collection(four_c, four_d, ace_c, nine_c, three_d)

        assert not smaller_collection > bigger_collection

    def test_gt_HighCard_whenEqual(self):
        bigger_collection = Card_Collection(queen_c, jack_c, seven_d, six_d, three_c)
        smaller_collection = Card_Collection(queen_d, jack_d, seven_h, six_c, three_d)

        assert not smaller_collection > bigger_collection
        assert not bigger_collection > smaller_collection

    def test_lt_HighCard_whenSmaller(self):
        bigger_collection = Card_Collection(ten_d, nine_c, eight_c, five_c, three_h)
        smaller_collection = Card_Collection(ten_d, nine_h, seven_h, six_d, three_d)

        assert smaller_collection < bigger_collection

    def test_lt_set_whenSmaller(self):
        bigger_collection = Card_Collection(ten_d, ten_h, eight_c, five_c, three_h)
        smaller_collection = Card_Collection(four_c, four_d, ace_c, king_c, queen_c)

        assert smaller_collection < bigger_collection

    def test_lt_HighCard_whenGreater(self):
        bigger_collection = Card_Collection(ten_d, nine_c, eight_c, five_c, three_h)
        smaller_collection = Card_Collection(ten_d, nine_h, seven_h, six_d, three_d)

        assert not bigger_collection < smaller_collection

    def test_lt_HighCard_whenEqual(self):
        bigger_collection = Card_Collection(queen_c, jack_c, seven_d, six_d, three_c)
        smaller_collection = Card_Collection(queen_d, jack_d, seven_h, six_c, three_d)

        assert not smaller_collection < bigger_collection
        assert not bigger_collection < smaller_collection


class Test_Deck:

    def test_BaseDeck_has52Cards(self):
        deck = Deck()
        assert len(deck.cards) == 52


class Test_Board:

    def test_flop_worksAsExpected(self):
        deck = Deck()
        board = Board()

        board.deal_flop(deck)

        assert len(board.cards) == 3
        assert len(deck.cards) == 49

        for card in board.cards:
            assert card not in deck.cards

