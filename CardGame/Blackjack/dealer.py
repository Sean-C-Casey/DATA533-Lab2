from ..Cards.card import Card
from ..Cards.deck import Deck
from ..Cards.hand import Hand
from .money import Money
from .person import Person


class Dealer(Person):
    def __init__(self, hand: Hand) -> None:
        self.hand = Hand()
