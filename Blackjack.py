#blackjack project
from random import*

suits = ('clubs','diamonds','hearts','spades')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11 }

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:

    def __init__(self,num_of_decks=1):

        self.num_of_decks = num_of_decks
        self.all_cards = []

        for i in range(num_of_decks):
            for suit in suits:

                for rank in ranks:
                    created_card = Card(suit, rank)
                    self.all_cards.append(created_card)
    
    def shuffle_deck(self):
        shuffle(self.all_cards)
    
    def return_to_deck(self,lst):
        self.lst = lst
        self.all_cards.extend(lst)
    
    def deal_one(self):
        return self.all_cards.pop(0)

class Hand:
#holds card objects and provides method for returning the sum of values
    def __init__(self):

        self.cards = []
        
    def show_hand(self):
        for i in range(len(self.cards)):
            print(self.cards[i])

    def add(self,card):

        self.cards.append(card)

    def rm(self):

        return self.cards.pop()

    def display(self):
        for i in self.cards:
            print(i)

    def get_sum(self):

        sum = 0

        for i in self.cards:
            if i.rank == 'Ace':
                if sum + 11 > 21:
                    i.value = 1
                elif sum + 11 <= 21:
                    i.value = 11
            sum += i.value
            
        return sum 
     

    
class Player:

    def __init__(self,name,bankroll = 500):  
        
        self.name = name
        self.bankroll = bankroll
    
    def win(self, amount):
        self.bankroll += amount

    def lose(self,amount):
        self.bankroll -= amount
        


 #Game Logic--------------------------------------------------------------------------------------------------------------------------------   
game_on = True

#instantiate an object that will represent a stack of say 5 decks
deck = Deck(1)
deck.shuffle_deck()

#declare an empty list for a discard pile
discard = []

#declare a variable for the pot
pot = 0

#ask for the players name
print('Please enter player name')
name = input()

#instantiate player class object
player = Player(name)

#instantiate Dealer class object
dealer = Player('Dealer', float('inf'))

#instantiate two hand objects for the player and the dealer
player_hand = Hand()
dealer_hand = Hand()

#create a function that will move cards to the discard pile
def move_to_discard(h):
    for i in range(len(h.cards)):
        discard.append(h.rm())

while game_on:
    #Check if player is out of money
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if player.bankroll == 0:
        print(f"{player.name}'s bankroll = {player.bankroll}. The house always wins.")
        game_on = False
        print("press enter to close")
        input()
        break
        

    

    #Ask player to place a bet, establish the pot
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    invalid_pot = True
    while invalid_pot == True:
        print(f"{player.name} balance: {player.bankroll}")
        print(f"{player.name} please place your bet. Enter q to quit")
        inpt = input()
        if inpt == 'q':
            print(f"Final score: {player.bankroll}")
            input()

        inpt = int(inpt)
        if inpt <= player.bankroll:
            invalid_pot = False
            pot += inpt
        else:
            print("Not enough chips.")
    print(f'{player.name} bets {pot}')

    
    #deal each player an initial hand. First check if the deck is empty. if empty, return cards from the discard pile and reshuffle.
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if len(deck.all_cards) < 1:
        deck.return_to_deck(discard)
        deck.shuffle_deck()
    
    for i in range(2):    
        player_hand.add(deck.deal_one())
        dealer_hand.add(deck.deal_one())



    #Display the player's hand and one card from the dealer
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    print(f"-------{player.name} has a(n): ")
    for i in player_hand.cards:
        print(i.rank)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    print("-------Dealer showing a(n)")
    for i in dealer_hand.cards[1:]:
        print(i.rank)
    print(("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"))

    
    #Player's Turn
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    player_loop = True
    player_bust = False
    player_blackjack = False
    while player_loop == True:
        #player gets blackjack
        if player_hand.get_sum() == 21 and len(player_hand.cards) == 2:
            print("Blackjack!")
            player.win(pot)
            pot = 0
            move_to_discard(player_hand)
            move_to_discard(dealer_hand)
            player_loop = False
            player_blackjack = True
        #player busts   
        elif player_hand.get_sum() > 21:
            print(f"{player.name} has {player_hand.get_sum()}. Bust...")
            player.lose(pot)
            pot = 0
            move_to_discard(player_hand)
            move_to_discard(dealer_hand)
            player_loop = False
            player_bust = True
        #ask if player wants to hit or stay
        else:
            print(f"{player.name} has {player_hand.get_sum()}")
            print("hit or stay? (h/s) -------")
            inpt = input()
            
            #player stays
            if inpt == 's':
                print(f"{player.name} stays.")
                player_loop = False
            
            # player hits
            elif inpt == 'h':
                
                #---------------------------------------
                #Check to make sure the deck isn't empty
                if len(deck.all_cards) < 1:
                    deck.return_to_deck(discard)
                    deck.shuffle_deck()
                    discard.clear()
                #---------------------------------------
                    

                #---------------------------------------
                #add a card from the deck to the player's hand and reprint hand
                player_hand.add(deck.deal_one())    
                print(f"-------{player.name} showing ")
                for i in player_hand.cards:
                    print(i.rank)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
   
            else:
                print('invalid entry')
    
    #Dealer's Turn
#--------------------------------------------------------------------------------------------------------------------------
    dealer_loop = True

    while dealer_loop == True and player_bust == False and player_blackjack == False:
        
        #show dealers full hand
        print("-------Dealer showing ")
        for i in dealer_hand.cards:
            print(i.rank)

        #dealer blackjack
        if dealer_hand.get_sum() == 21 and len(dealer_hand.cards) == 2:
            print("Dealer has blackjack.")
            pot = 0
            move_to_discard(player_hand)
            move_to_discard(dealer_hand)
            player.lose(pot)
            dealer_loop = False

        elif dealer_hand.get_sum() > 21:
            print("Dealer busts.")
            player.win(pot)
            pot = 0
            move_to_discard(player_hand)
            move_to_discard(dealer_hand)
            dealer_loop = False

        else:
          
            #Check to make sure the deck isn't empty
            if len(deck.all_cards) < 1:
                deck.return_to_deck(discard)
                deck.shuffle_deck()
                discard.clear()
            #---------------------------------------
                    
            #dealer hits
            if  dealer_hand.get_sum() < 17:
                print('Dealer hits.')
                dealer_hand.add(deck.deal_one())
            
            #dealer stays
            else:
                print("Dealer stays.")
                print(f"-------Dealer has {dealer_hand.get_sum()} ")
                for i in dealer_hand.cards:
                    print(i.rank)
 
                dealer_loop = False


    if len(player_hand.cards) != 0 and len(dealer_hand.cards) != 0:

        #player wins
        if player_hand.get_sum() > dealer_hand.get_sum():
            print(f"{player.name} wins the hand.")
            player.win(pot)
            pot = 0
            move_to_discard(player_hand)
            move_to_discard(dealer_hand)
            
        
        #dealer wins
        else: 
            print(f"{dealer.name} wins the hand.")
            player.lose(pot)
            pot = 0
            move_to_discard(player_hand)
            move_to_discard(dealer_hand)






                
            
 
