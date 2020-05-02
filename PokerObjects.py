from enum import Enum, auto
from random import shuffle

allowed_values = [x for x in range(2, 15)]

value_strings = {
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


class Card_Collection:

    def __init__(self, *cards: Card):
        self.cards = []

        if cards is not None:
            self.cards += cards

    def __str__(self):
        return ', '.join([str(c) for c in self.cards])

    def add(self, *cards):
        if cards is not None:
            self.cards += cards


class Hand(Card_Collection):
    def __init__(self, cards=()):
        super().__init__(*cards)


class Board(Card_Collection):
    def __init__(self, cards=()):
        super().__init__(*cards)


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


if __name__ == "__main__":
    d = Deck()
    print(len(d.cards))
    print(d.cards[0])
    print(d)
    h = Hand()
    d.deal(h, count=2)
    print(h)
