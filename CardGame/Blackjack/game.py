from signal import signal, SIGINT
from sys import exit

from .money import Money
from .person import Dealer, Player
from ..Cards.deck import Deck


class Game():
    def __init__(self, num_players: int = 1) -> None:
        if not isinstance(num_players, int):
            raise TypeError("'num_players' must be an integer")
        if num_players < 1:
            raise ValueError("'num_players' must be a positive value")
        signal(SIGINT, ctrl_C_handler)

        self.num_players = num_players
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer = Dealer(self.deck)
        self.players = [Player(name=f"Player {i + 1}", money=Money()) for i in range(num_players)]

        for player in self.players:
            player.addToHand(self.dealer.dealHand(2))

        self.dealer.hand = self.dealer.dealHand(1)

    def newRound(self) -> None:
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer = Dealer(self.deck)

        for player in self.players:
            player.hand = self.dealer.dealHand(2)

        self.dealer.hand = self.dealer.dealHand(1)

    def run(self) -> None:
        if self.num_players == 1:
            self.__run_singleplayer()
        else:
            self.__run_multiplayer()
    
    def __run_multiplayer(self) -> None:
        live_table = True
        while live_table is True:
            self.newRound()
            # betting_pool = 0
            for i, player in enumerate(self.players):
                print(f"{player.name}. ", end="")
                print(player.showMoney())
                # betting_pool += player.money.bet()
                player.money.bet()
            print("\nDealer's hand: ", self.dealer.displayHand())
            self.dealer.addCardToHand(self.dealer.dealCard())
            for i, player in enumerate(self.players):
                print(f"{player.name}'s hand: ", player.displayHand())
            
            # Phase where players hit or stand
            not_busted = set()
            blackjacks = set()
            print("\n", end="")
            for i, player in enumerate(self.players):
                # print(f"Player {i + 1}. ")
                print(f"{player.name}. ")
                hit = player.hit_stand()
                while hit is True:
                    player.addCardToHand(self.dealer.dealCard())
                    print("Your hand: ", player.displayHand())

                    if player.getHandPoints() > 21:
                        print("You go bust!")
                        player.discardHand()
                        hit = False
                    elif player.getHandPoints() == 21:
                        print("That's a blackjack!")
                        print(f"You win ${1.5 * player.money.wager}")
                        hit = False
                    else:
                        hit = player.hit_stand()
                
                print("\n", end="")
                if player.getHandPoints() < 21:
                    not_busted.add(player)
                elif player.getHandPoints() == 21:
                    blackjacks.add(player)            

            # Dealer's turn to hit or stand now
            dealer_hit = self.dealer.hit_stand()
            while dealer_hit == True:
                self.dealer.addCardToHand(self.dealer.dealCard())
                dealer_hit = self.dealer.hit_stand()
            dealer_points = self.dealer.getHandPoints()

            # Done dealing cards, compare scores now
            for i, player in enumerate(self.players):
                if player in blackjacks:
                    # Blackjack!
                    player.money.payout(2.5)
                elif player in not_busted:
                    if player.getHandPoints() > dealer_points:
                        # Winners!
                        print("Dealer's hand: ", self.dealer.displayHand())
                        print(f"{player.name}'s hand: ", player.displayHand())
                        print(f"You won ${player.money.wager}! \n")
                        player.money.payout(2)
                    elif player.getHandPoints() == dealer_points:
                        # Tie!
                        print("Dealer's hand: ", self.dealer.displayHand())
                        print(f"{player.name}'s hand: ", player.displayHand())
                        print("That's a tie. \n")
                        player.money.payout(1)
                    else:
                        # Lose - beaten by dealer
                        print(f"The dealer beats {player.name} \n")
                        player.money.payout(0)
                else:
                    # Lose - went bust
                    player.money.payout(0)
                
            # Determine whether game is finished or not
            updated_player_list = []
            for i, player in enumerate(self.players):
                if player.money.value <= 0:
                    print(f"{player.name} has ${player.money.value}")
                    print("Game Over for you:(")
                elif player.money.value >= Money.win_amount:
                    print(f"{player.name} has ${player.money.value}\nYou win!")
                else:
                    # Didn't win or lose, so still in the game
                    updated_player_list.append(player)
            self.players = updated_player_list
            if len(updated_player_list) == 0:
                live_table = False

    def __run_singleplayer(self) -> None:
        player = self.players[0]
        live_table = True
        while live_table is True:
            self.newRound()
            print(player.showMoney())
            bet = player.money.bet()
            print("Dealer's hand: ", self.dealer.displayHand())
            print("Your hand: ", player.displayHand(), "\n")
            self.dealer.addCardToHand(self.dealer.dealCard())

            # Phase where player hits or stands
            hit = player.hit_stand()
            while hit is True:
                player.addCardToHand(self.dealer.dealCard())
                print("Your hand: ", player.displayHand())

                if player.getHandPoints() > 21:
                    print("You go bust!")
                    player.discardHand()
                    hit = False
                elif player.getHandPoints() == 21:
                    print("That's a blackjack!")
                    hit = False
                else:
                    hit = player.hit_stand()
            player_points = player.getHandPoints()

            # Dealer's turn to hit or stand now
            if player_points > 0 and player_points != 21:
                dealer_hit = self.dealer.hit_stand()
                while dealer_hit == True:
                    self.dealer.addCardToHand(self.dealer.dealCard())
                    dealer_hit = self.dealer.hit_stand()
            dealer_points = self.dealer.getHandPoints()
            
            # Finished dealing cards, not compare hand scores
            if player_points == dealer_points:
                print("Dealer's hand: ", self.dealer.displayHand())
                print("Your hand: ", player.displayHand())
                print("That's a tie. \n")
                # player.money.payout(bet, 1)
                player.money.payout(1)
            elif player_points == 21:
                print(f"You win ${1.5 * bet}")
                # player.money.payout(bet, 2.5)
                player.money.payout(2.5)
            elif player_points > dealer_points:
                print("Dealer's hand: ", self.dealer.displayHand())
                print("Your hand: ", player.displayHand())
                print(f"You won ${bet}! \n")
                # player.money.payout(bet, 2)
                player.money.payout(2)
            else:
                print("The dealer wins that round. \n")

            # Determine if whether game is won, lost, or still in progress
            if player.money.value <= 0:
                print(f"You have ${player.money.value}\nGame Over :(")
                self.players = [Player(money=Money()) for i in range(self.num_players)]
                live_table = False
            elif player.money.value >= Money.win_amount:
                print(f"You have ${player.money.value}\nYou win!")
                self.players = [Player(money=Money()) for i in range(self.num_players)]
                live_table = False

def ctrl_C_handler(signum, stack_frame):
    print("\n\nCtrl-C received. Ending program. Have a nice day! ")
    exit(0)