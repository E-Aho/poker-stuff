from PokerObjects import Deck

class Test_Deck:

    def test_init(self):
        d = Deck()
        assert len(d.cards) == 52
