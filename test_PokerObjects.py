from PokerObjects import *


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


class Test_Deck:

    def test_Base_deck_has_52_cards(self):
        deck = Deck()
        assert len(deck.cards) == 52


class Test_Board:

    def test_flop_works_as_expected(self):
        deck = Deck()
        board = Board()

        board.deal_flop(deck)

        assert len(board.cards) == 3
        assert len(deck.cards) == 49

        for card in board.cards:
            assert card not in deck.cards
