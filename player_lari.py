import random
import operator

class BasePlayer(object):
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
            
            self.tricks_won = {}
            self.tricks_played = 0

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
        random.shuffle(self.hand)
        return self.hand.pop()
        
class PlayerLARIJr(BasePlayer):

    def __init__(self):
        super().__init__()

    def get_name(self):
        return "L.A.R.I JR."

    def play_card(self, lead, trick):
        # TODO: Implmemt
        pass

    def collect_trick(self, lead, winner, trick):
        # TODO: Implement
        super().collect_trick(lead, winner, trick)
        pass


