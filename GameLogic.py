from collections import Counter

from PokerObjects import *


def get_straight(input_cards: list):
    """
    Takes a list of cards, returns list of cards in straight (if a straight exists) or none
    This function will ignore suit.
    (E.g if two cards of same suit can be in a straight, will return either)
    """
    cards = sorted(input_cards, key=lambda c: -c.value)

    # remove duplicate value cards
    card_values = []
    for card in cards:
        if card.value in card_values:
            cards.remove(card)
        else:
            card_values.append(card.value)
    if len(cards) < 5:
        return None

    # add a lower variant if ace present
    if cards[0].value == 14:
        cards.append(Card(1, cards[0].suit))

    for start_index in range(len(cards) - 4):  # only care about 5 card straight

        subset = cards[start_index: start_index + 5]
        if all(subset[i].value == subset[i + 1].value + 1 for i in range(4)):  # found straight!

            # replace lower ace with original ace
            if subset[4].value == 1:
                subset[4] = cards[0]

            return subset

    return None


def find_strongest(cards: list):
    """Takes in a single hand, returns a scored hand"""

    # check if flush is present

    count_suits = Counter([c.suit for c in cards])

    for suit, count in count_suits.items():
        if count >= 5:
            flush_vals = sorted([card.value for card in cards if card.suit == suit])
            return flush_vals[0:5]


if __name__ == "__main__":
    d = Deck()

    b = Board()
    h = Hand()

    d.deal(h, count=3)
    d.deal(b, count=2)

    get_straight(b, h)
