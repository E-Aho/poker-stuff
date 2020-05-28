from collections import Counter

from PokerObjects import *


# NB: Methods assume that normal Texas Hold'em rules are used.
#
# Some methods may not return optimal hand in case of weird rules.
# E.g if there are 10+ cards in hand + board, where more than one straight or flush is possible.
# Or if there are 8 cards, it is possible that both a straight and full house are present,
# but these methods will not take that into account (short out after finding flush/straight)

def get_sorted_remainder(sets: list, all_cards: list):
    return sorted([c for c in all_cards if c not in sets], key=lambda c: -c.value)


def get_sorted_sets(cards: list):
    """
    Takes in cards, returns list of cards sorted first by size of set, then by value for sets of same size
    e.g for cards with values as follows,
    [14, 14, 13, 13, 13, 12, 11] => [13, 13 ,13 ,14, 14]
    [6, 2, 6, 2, 4, 4, 4] => [4, 4, 4, 6, 6, 2, 2]
    [2, 3, 4, 5, 6, 7] => []
    """
    value_counter = Counter([c.value for c in cards])
    sets = [c for c in cards if value_counter[c.value] > 1]
    return sorted(sets, key=lambda c: -(value_counter[c.value] + c.value / 100))


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

    if (flush := find_flush(cards)) is not None:
        if (straight_flush := get_straight(flush)) is not None:
            hand.best_5 = straight_flush
            hand.strength = 8
            return hand
        else:
            hand.best_5 = flush[0:5]
            hand.strength = 5
            return hand
    elif (straight := get_straight(cards)) is not None:
        hand.best_5 = straight
        hand.strength = 4
        return hand

    # no straights or flushes, now check for sets

    sets = get_sorted_sets(cards)

    if not sets:
        hand.best_5 = sorted(cards, key=lambda c: -c.value)[:5]
        hand.strength = 0
        return hand

    def handle_4_set():
        # must be 4 of a kind + high card
        four_of_a_kind = sets[:4]
        remainder = get_sorted_remainder(four_of_a_kind, cards)
        hand.best_5 = four_of_a_kind + [remainder[0]]
        hand.strength = 7
        return hand

    def handle_3_set():
        # either 3 of a kind or full house
        if len(sets) == 3:  # 3 of a kind
            three_of_a_kind = sets
            remainder = get_sorted_remainder(three_of_a_kind, cards)
            hand.best_5 = three_of_a_kind + remainder[:2]
            hand.strength = 3
            return hand
        else:  # full house
            hand.strength = 6
            hand.best_5 = sets[:5]  # Set has been sorted already to have best option in first 5 in get_sorted_sets
            return hand

    def handle_2_set():
        # either pair or 2 pair
        if len(sets) == 2:
            pair = sets
            remainder = get_sorted_remainder(pair, cards)
            hand.best_5 = pair + remainder[:3]
            hand.strength = 1
            return hand
        else:
            two_pair = sorted(sets, key=lambda c: -c.value)[:4]
            remainder = get_sorted_remainder(two_pair, cards)
            hand.best_5 = two_pair + [remainder[0]]
            hand.strength = 2
            return hand

    def no_set_error():
        raise Exception("No set found")

    def set_switcher(set_size: int):
        size_switch_case = {
            4: lambda: handle_4_set(),
            3: lambda: handle_3_set(),
            2: lambda: handle_2_set()
        }
        function = size_switch_case.get(set_size, lambda: no_set_error())
        return function()

    largest_count = max(count for _, count in Counter([c.value for c in cards]).items())

    return set_switcher(largest_count)


def have_same_best_5(hand_a: Hand, hand_b: Hand):
    return Card_Collection(*hand_a.best_5).has_same_values_as(Card_Collection(*hand_b.best_5))


def get_scoring_order(*hands: Hand):
    """takes in any number of hands, returns list of lists of hands in order of strength"""
    scoring_order = []
    for strength in range(8, -1, -1):
        if st := [hand for hand in hands if hand.strength == strength]:
            if len(st) == 1:
                scoring_order.append(st)
            else:  # group into lists based on best_5 of each hand

                list_current_strength = []
                while len(st) > 0:
                    sub_list = [equal_hand for equal_hand in st if have_same_best_5(st[0], equal_hand)]
                    st = [hand for hand in st if hand not in sub_list]
                    list_current_strength.append(sub_list)

                # sort current strength list in order of the card size in the sublists
                # (using overridden __gt__ and __lt__ for Card_Collection)
                list_current_strength.sort(key=lambda arr: Card_Collection(*arr[0].best_5), reverse=True)
                scoring_order += list_current_strength

    return scoring_order


if __name__ == "__main__":
    d = Deck()

    b = Board()
    h = Hand()

    d.deal(h, count=3)
    d.deal(b, count=2)
