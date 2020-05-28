from enum import Enum, auto
from random import shuffle

allowed_values = [x for x in range(2, 15)]

value_strings = {
    1: "Ace",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9",
    10: "10",
    11: "Jack",
    12: "Queen",
    13: "King",
    14: "Ace"
}

strength_strings = {
    0: "High card",
    1: "Pair",
    2: "Two pair",
    3: "3 of a kind",
    4: "Straight",
    5: "Flush",
    6: "Full house",
    7: "4 of a kind",
    8: "Straight flush"
}


class Suit(Enum):
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()


class Card:
    def __init__(self, value: int, suit: Suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return "{val} of {suit}".format(val=value_strings[self.value], suit=self.suit.name.capitalize())

    def __eq__(self, other_obj):
        if isinstance(other_obj, Card):
            return (self.suit, self.value) == (other_obj.suit, other_obj.value)
        else:
            return False

    def __lt__(self, other):
        if isinstance(other, Card):
            if self.value < other.value:
                return 1
            else:
                return 0
        elif isinstance(other, int):
            if self.value < other:
                return 1
            else:
                return 0
        else:
            raise TypeError(f"< not supported for types Card and {type(other).__name__}")

    def __gt__(self, other):
        if isinstance(other, Card):
            if self.value > other.value:
                return 1
            else:
                return 0
        elif isinstance(other, int):
            if self.value > other:
                return 1
            else:
                return 0
        else:
            raise TypeError(f"< not supported for types Card and {type(other).__name__}")


class Card_Collection:
    """Base class for objects which will hold a list of cards"""

    def __init__(self, *cards: Card):
        self.cards = []

        if cards is not None:
            self.cards += cards

    def __str__(self):
        return ', '.join([str(c) for c in self.cards])

    def add(self, *cards):
        if cards is not None:
            self.cards += cards

    def sort_by_val(self):
        """Sorts the cards in this object in value from largest to smallest"""
        self.cards = sorted(self.cards, key=lambda card: -card.value)

    def get_sorted_cards(self):
        """Returns a sorted array of cards, but does not affect the original object"""
        return sorted(self.cards, key=lambda card: -card.value)

    def __gt__(self, other_obj):
        """
        Compares cards, from largest to smallest in each card collection,
        to see which object has the larger largest cards.
        e.g K,5,4,3,2 would be bigger than 10,9,7,6,5, as K > 10
        Raises error if the objects are of different size or type
        NB: Does not sort cards, assumes card order is relevant. (e.g 10, 10. 2 > 9, 9. ace)
        """

        if not isinstance(other_obj, Card_Collection):
            raise TypeError(f"< not supported between instances of Card_Collection and {type(other_obj).__name__}")

        if (num_cards := len(my_cards := self.cards)) != len(other_cards := other_obj.cards):
            raise ValueError(f"Input card collections are not the same length.")

        for i in range(num_cards):
            if my_cards[i] > other_cards[i]:
                return 1
            elif my_cards[i].value != other_cards[i].value:
                return 0

        return 0  # All cards are equal, so not bigger

    def __lt__(self, other_obj):
        """
        Compares cards, from largest to smallest in each card collection,
        to see which object has the smaller largest cards.
        e.g K,5,4,3,2 would be bigger than 10,9,7,6,5, as K > 10
        Raises error if the objects are of different size or type
        NB: Does not sort cards, assumes card order is relevant. (e.g 10, 10. 2 > 9, 9. ace)
        """

        if not isinstance(other_obj, Card_Collection):
            raise TypeError(f"< not supported between instances of Card_Collection and {type(other_obj).__name__}")

        if (num_cards := len(my_cards := self.cards)) != len(other_cards := other_obj.cards):
            raise ValueError(f"Input card collections are not the same length.")

        for i in range(num_cards):
            if my_cards[i] < other_cards[i]:
                return 1
            elif my_cards[i].value != other_cards[i].value:
                return 0

        return 0  # All cards are equal, so not smaller

    def has_same_values_as(self, other_obj):

        if not isinstance(other_obj, Card_Collection):
            raise TypeError(f"< not supported between instances of Card_Collection and {type(other_obj).__name__}")

        if (num_cards := len(my_cards := self.get_sorted_cards())) != len(other_cards := other_obj.get_sorted_cards()):
            raise ValueError(f"Input card collections are not the same length.")

        if ([c.value for c in my_cards]) != ([c.value for c in other_cards]):
            return False
        return True


class Hand(Card_Collection):
    """
    Object that serves as proxy for player.
    Contains both that players card and the strength of their cards with the board
    """

    def __init__(self, *cards):
        super().__init__(*cards)

        self.strength = 0
        self.best_5 = []
        self.name = ""

    def withStrength(self, strength: int):
        self.strength = strength
        return self

    def __str__(self):
        str_arr = [str(card) for card in self.get_sorted_cards()]
        return ", ".join(str_arr)

    def __repr__(self):
        return str(self)


class Deck(Card_Collection):
    def __init__(self):
        super().__init__()
        self.cards = [Card(v, s) for v in allowed_values for s in Suit]

    def shuffle(self):
        shuffle(self.cards)

    def deal(self, *targets, count=1):
        self.shuffle()
        for target in targets:
            target.add(*[self.cards.pop() for _ in range(count)])


class Board(Card_Collection):
    def __init__(self, *cards):
        super().__init__(*cards)

    def deal_flop(self, deck: Deck):
        deck.deal(self, count=3)


class Player:
    def __init__(self):
        self.chips = 0
        self.hand = Hand()


class Table:
    def __init__(self):
        self.hands = []
        self.board = []
        self.showdown_order = []
    # TODO: finish meta-game objects


if __name__ == "__main__":
    d = Deck()
    print(len(d.cards))
    print(d.cards[0])
    print(d)
    h = Hand()
    d.deal(h, count=2)
    print(h)
