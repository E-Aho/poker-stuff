from unittest import TestCase

from PokerObjects import *


class Test_Card_Collection(TestCase):

    def test_noCards_constructsAsExpected(self):
        card_collection = Card_Collection()

        self.assertEqual(card_collection.cards, [])

    def test_withCardList_constructsAsExpected(self):
        a = Card(10, Suit.DIAMONDS)
        b = Card(5, Suit.SPADES)
        cards = [a, b]

        card_collection = Card_Collection(*cards)

        self.assertTrue(len(card_collection.cards) == 2)

    def test_toString_returnsAsExpected(self):
        a = Card(13, Suit.SPADES)
        b = Card(2, Suit.CLUBS)
        c = Card(14, Suit.DIAMONDS)

        cards = [a, b, c]
        card_collection = Card_Collection(*cards)

        self.assertEqual('King of Spades, 2 of Clubs, Ace of Diamonds', str(card_collection))
