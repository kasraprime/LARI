import random
import operator
from spades_state import SpadesState
from mcts import mcts
from util import *
from copy import copy
from game_engine import Deck

MCTS_SEARCH_TIME = 12000
NUM_SIMS = 5
DEBUG_JR = True

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
            self._score = get_player_score(self.tricks_won, self.name)
            
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
            try:
                idx = self.hand.index('2C')
                card = self.hand.pop(idx)
                return card
            except ValueError:
                pass

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
        self.cards_played = []
        self.oppo_hand_info = {}
        super().__init__()

    def get_name(self):
        return self.name

    def gen_hands(self, lead, trick):
        player_order = order_players(self.player_names, lead)
        deck = Deck()

        # Remove cards that we know opponents can't have.
        deck.remove_cards(self.hand)
        deck.remove_cards(self.cards_played)
        deck.remove_cards(trick)
        hands = {}

        # TODO: CONSTRAINED SIM HANDS IS NOT WORKING.
        # CURRENT APPROACH CAN RESULT IN NOT ALL CARDS BEING DEALT DUE TO
        # CONSTRAINTS NOT BEING SATISFIED IN THE CORRECT ORDER.
        # HACk SOLUTION IS TO REMOVE CONSTRAINTS IN GET_CONSTR_CARDS()
        our_idx = player_order.index(self.name)
        for idx, p in enumerate(player_order):
            if idx < our_idx:
                hand_info = self.oppo_hand_info[p]
                # Players before us have contributed to the current trick.
                hand_size = len(self.hand) - 1
                hand = deck.get_constrained_cards(hand_info, hand_size)
                deck.remove_cards(hand)
                hands[p] = hand
            elif idx > our_idx:
                hand_info = self.oppo_hand_info[p]
                hand_size = len(self.hand)
                hand = deck.get_constrained_cards(hand_info, hand_size)
                deck.remove_cards(hand)
                hands[p] = hand
            else:
                hands[p] = self.hand
            
        return hands

    def play_card(self, lead, trick):
        # If we have a 2C, play it (as it should always be played first).
        try:
            idx = self.hand.index('2C')
            card = self.hand.pop(idx)
            return card
        except ValueError:
            pass

        # TODO: Thoughts on adding hard coded rules here?
        #   - If we're last to play, play the lowest card that can win

        player_order = order_players(self.player_names, lead)
        idx = player_order.index(self.name)
        best_plays = []
        if DEBUG_JR: print("--------------_ENTERING THE MONTE CARLO ZONE----------------")

        # TODO: Parallelize this for better performance
        for x in range(NUM_SIMS):
            sim_hands = self.gen_hands(lead, trick)
            for sh in sim_hands.items():
                if DEBUG_JR:
                    print("Player: " + sh[0] + " => " + str(sh[1]))

            root_state = SpadesState(self.name, player_order, trick, sim_hands, copy(self.tricks_won))

            _mcts = mcts(timeLimit=MCTS_SEARCH_TIME)
            best_action = _mcts.search(initialState=root_state)

            best_play = best_action[idx]
            if DEBUG_JR: print("\tBEST PLAY: " + best_play)
            best_plays.append(best_play)

        if DEBUG_JR: print("Best plays => " + str(best_plays)) 
        best_play = random.choice(best_plays)    
        if DEBUG_JR: print("Best Play Chosen => " + best_play)
        self.hand.pop(self.hand.index(best_play))
        return best_play

    def new_hand(self, names):
        super().new_hand(names)
        for n in names:
            # Can the opponent have cards of the suits in their hand?
            self.oppo_hand_info[n] = {'S': True, 'C': True, 'H': True, 'D': True}

    def _clear(self):
        self.cards_played = []
        self.oppo_hand_info = {}
        super()._clear()

    def collect_trick(self, lead, winner, trick):
        # Update which cards have been played
        self.cards_played = self.cards_played + trick

        # Update information about opponent hands (if possible).
        player_order = order_players(self.player_names, lead)
        lead_suit = get_suit(trick[0])
        for idx, c in enumerate(trick[1:]):
            # TODO: when/if trump is introduced, this will need to update.
            if get_suit(c) != lead_suit:
                oppo_player = player_order[idx]
                # AHA! They no longer have any cards of lead_suit.
                self.oppo_hand_info[oppo_player][lead_suit] = False

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
        try:
            idx = self.hand.index('2C')
            card = self.hand.pop(idx)
            return card
        except ValueError:
            pass

        #if we are leading the trick, play the lowest card in our hand
        if lead == self.get_name():
            card = get_min_card(self.hand)
        else:
            #get the suits for the trick
            lead_suit = get_suit(trick[0])
            #get all the cards in our hand that matches the suit of the trick
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
        super().collect_trick(lead, winner, trick)
        pass
