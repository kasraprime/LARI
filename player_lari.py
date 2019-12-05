import random
import operator
from copy import copy
from spades_state import SpadesState
from mcts import mcts
from util import *

MCTS_SEARCH_TIME = 2*1000
NUM_SIMS = 5
DEBUG_JR = False

class Player(object):

	def __init__(self):
		self.name = "L.A.R.I"
		self.cards_played = []
		self.oppo_hand_info = {}
		self._clear()
		
	def _clear(self):
		"""
		Clear any state.
		"""
		self._score = 0
		self.hand = []
		self.cards_played = []
		self.oppo_hand_info = {}
		self.tricks_won = {}
		self.tricks_played = 0
		
	def get_name(self):
		return self.name
	
	def get_tricks_won(self):
		return self.tricks_won[self.name]
		
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
		#   - Play Ace of Spades if we have it
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
		self.player_names = names
		self._clear()

		for n in names:
			self.tricks_won[n] = 0
			# Can the opponent have cards of the suits in their hand?
			self.oppo_hand_info[n] = {'S': True, 'C': True, 'H': True, 'D': True}

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

		self.tricks_played = self.tricks_played + 1
		self.tricks_won[winner] = self.tricks_won[winner] + 1

		# One hand is 13 tricks.
		if self.tricks_played == 13:
			self._score = get_player_score(self.tricks_won, self.name)
		
		
	def score(self):
		"""
		Calculates and returns the score for the game being played.
		"""
		return self._score

