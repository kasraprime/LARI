import random
import operator

def get_all_cards_suit(suit):
    if suit == "D":
        cards = {"2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "TD", "JD", "QD", "KD", "AD"}
    elif suit == "S":
        cards = {"2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "TS", "JS", "QS", "KS", "AS"}
    elif suit == "H":
        cards = {"2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "TH", "JH", "QH", "KH", "AH"}
    elif suit == "C":
        cards = {"2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "TC", "JC", "QC", "KC", "AC"}
    else:
        cards = set()

    return cards

def get_suit(card):
    return card[1:]

def get_rank(card):
    rank = 0
    r = card[:1]
    if (r == "A"):
        rank = 14
    elif (r == "K"):
        rank = 13
    elif (r == "Q"):
        rank = 12
    elif (r == "J"):
        rank = 11
    elif (r == "T"):
        rank == 10
    else:
        rank = int(r)
    
    return rank

def get_min_card(cards):
	min_val = get_rank(list(cards)[0])
	min_card = list(cards)[0]
	
	for c in cards:
		rank = get_rank(c)
		if rank < min_val:
			min_val = rank
			min_card = c
		
	return min_card

def get_max_card(cards):
	max_val = get_rank(list(cards)[0])
	max_card = list(cards)[0]
	
	for c in cards:
		rank = get_rank(c)
		if rank > max_val:
			max_val = rank
			max_card = c
		
	return max_card


class Player(object):
    """
    Project Player interface.
    """
    def __init__(self):
        pass

    def get_name(self):
        pass

    def get_hand(self):
        pass

    def new_hand(self, names):
        pass

    def add_cards_to_hand(self, cards):
        pass

    def play_card(self, lead, trick):
        pass

    def collect_trick(self, lead, winner, trick):
        pass

    def score(self):
        pass

class BasePlayer(Player):
    """
    Implements functionality shared by all players.
    """
    def __init__(self):
        self._clear()
        pass

    def _clear(self):
        """
        Clear any state.
        """
        self._score = 0
        self.hand = []
        self.tricks_won = {}
        self.tricks_played = 0
    
    def play_card(self, lead, trick):
        """
        Takes a a string of the name of the player who lead the trick and
        a list of cards in the trick so far as arguments.

        Returns a two character string from the agents hand of the card to be played
        into the trick.
        """
        pass

    def collect_trick(self, lead, winner, trick):
        """
        Takes three arguements. Lead is the name of the player who led the trick.
        Winner is the name of the player who won the trick. And trick is a four card
        list of the trick that was played. Should return nothing.
        """
        self.tricks_played = self.tricks_played + 1
        self.tricks_won[winner] = self.tricks_won[winner] + 1

        # One hand is 13 tricks.
        if self.tricks_played == 13:
            sorted_tricks_won = sorted(self.tricks_won.items(), key=operator.itemgetter(1), reverse=True)
            our_place = list(map(lambda x: x[0], sorted_tricks_won)).index(self.name)
            # Get places.
            first_place_name = sorted_tricks_won[0][0]
            second_place_name = sorted_tricks_won[1][0]
            third_place_name = sorted_tricks_won[2][0]
            fourth_place_name = sorted_tricks_won[3][0]

            if self.tricks_won[first_place_name] == self.tricks_won[second_place_name]: # Tie
                if self.tricks_won[second_place_name] == self.tricks_won[third_place_name]: # Three way tie
                    if our_place < 3: # We tied with two others.
                        self._score = 3
                else:
                    if our_place < 2: # We tied with someone else.
                        self._score = 5
            else: # Single winner
                if our_place < 1: # We won!
                    self._score = 11
            
    def get_name(self):
        """
        Returns a string of the agent's name
        """
        return self.name

    def get_hand(self):
        """
        Returns a list of two character strings reprsenting cards in the agent's hand
        """
        return self.hand

    def get_tricks_won(self):
        return self.tricks_won[self.name]

    def new_hand(self, names):
        """
        Takes a list of names of all agents in the game in clockwise playing order
        and returns nothing. This method is also responsible for clearing any data
        necessary for your agent to start a new round.
        """
        self.player_names = names
        self._clear()
        for n in names:
            self.tricks_won[n] = 0

    def add_cards_to_hand(self, cards):
        """
        Takes a list of two character strings representing cards as an argument
        and returns nothing.
        This list can be any length.
        """
        self.hand.extend(cards)

    def score(self):
        """
        Calculates and returns the score for the game being played.
        """
        return self._score

class PlayerRandom(BasePlayer):

    def __init__(self):
        self.name = "RANDOM_" + str(random.randint(1,9999999))
        self._clear()
        super().__init__()

    def play_card(self, lead_player, trick):
        if lead_player == self.name: 
            random.shuffle(self.hand)
            card = self.hand.pop()
        else:
            suit = trick[0][1:]
            random.shuffle(self.hand)
            x = 0
            for i in range(len(self.hand)):
                if self.hand[i][1:] == suit:
                    x = i
                    break
            card = self.hand.pop(x)
            
        return card
        
class PlayerLARIJr(BasePlayer):

    def __init__(self):
        self.name = "L.A.R.I JR."
        super().__init__()

    def get_name(self):
        return self.name

    def play_card(self, lead, trick):
        # TODO: Implmemt
        pass

    def collect_trick(self, lead, winner, trick):
        # TODO: Implement
        super().collect_trick(lead, winner, trick)
        pass

class PlayerPassiveLARI(BasePlayer):

    def __init__(self):
        super().__init__()
        self.name = "1up L.A.R.I"
        self._clear()

    def get_name(self):
        return self.name

    def play_card(self, lead, trick):
        #if we are leading the trick, play the lowest card in our hand
        if lead == self.get_name():
            card = get_min_card(self.hand)
        else:
            #get the suits for the trick
            lead_suit = get_suit(trick[0])
            #get all the vards in out hand that matches the suit of the trick
            valid_cards = set(self.hand).intersection(get_all_cards_suit(lead_suit))
            #if we do not have any cards of that suit play the lowest card in our hand
            if len(valid_cards) == 0:
                card = get_min_card(self.hand)
            else:
                #find the currently winng card in the trick
                max_card_in_trick = get_max_card(set(trick).intersection(get_all_cards_suit(lead_suit)))
                #find the highset card in our hand
                max_card_in_hand = get_max_card(valid_cards)

                #if we cannot win the trick play the lowest card of that suit in our hand
                if(get_rank(max_card_in_trick) > get_rank(max_card_in_hand)):
                    card = get_min_card(valid_cards)
                else:
                    #find the lowest card in our hand that wins the trick as it currently is
                    for c in valid_cards:
                        rank = get_rank(c)
                        if rank < get_rank(max_card_in_hand) and rank > get_rank(max_card_in_trick):
                            max_card_in_hand = c

                    card = max_card_in_hand

        #remove the card from our hand
        self.hand.remove(card)

        return card

    def collect_trick(self, lead, winner, trick):
        # TODO: Implement
        super().collect_trick(lead, winner, trick)
        pass
