# ~/usr/bin/env python3
from CardGame.Blackjack.money import Money
from CardGame.Cards.card import Card
from CardGame.Cards.deck import Deck
from CardGame.Cards.hand import Hand
from CardGame.Blackjack.person import Person


def demo():
    print("Demoing the game...")
    deck = Deck()
    deck.shuffle()
    # hand = Hand(deck.drawCards(5))
    hand = Hand([Card("A", "spades"), Card("A", "hearts")])
    hand.addCards(deck.drawCards(3))
    money = Money()
    player = Person(hand=hand, money=money)
    print(player.hand)
    print(player.getHandPoints())
    print(player.showMoney())


if __name__ == "__main__":
    demo()
