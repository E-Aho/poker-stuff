from collections import Counter

from PokerObjects import *

"""
NB: Methods assume that normal Texas Hold'em rules are used.

Some methods may not return optimal hand in case of weird rules.
E.g if there are 10+ cards in hand + board, where more than one straight or flush is possible.
"""

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


def find_flush(input_cards: list):

    if len(input_cards) < 5:  # too few cards for flush
        return None

    suit_counter = Counter([c.suit for c in input_cards])
    for suit, suit_count in suit_counter.items():
        if suit_count >= 5:
            sorted_flush = sorted([c for c in input_cards if c.suit == suit], key=lambda c: -c.value)
            return sorted_flush

    return None


def find_strongest(hand: Hand, board: Board):
    """Takes in a single hand, returns a scored hand"""

    cards = hand.cards + board.cards

    if flush := find_flush(cards) is not None:
        if straight_flush := get_straight(flush) is not None:
            hand.best_5 = straight_flush
            hand.strength = 8
            return hand
        else:
            hand.best_5 = flush[0:5]
            hand.strength = 5
            return hand
    elif straight := get_straight(cards) is not None:
        hand.best_5 = straight
        hand.strength = 4






if __name__ == "__main__":
    d = Deck()

    b = Board()
    h = Hand()

    d.deal(h, count=3)
    d.deal(b, count=2)

