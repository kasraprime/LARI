import random
import operator
from copy import copy
from spades_state import SpadesState
from mcts import mcts
from util import *

MCTS_SEARCH_TIME = 500
DEBUG_JR = False

class Player(object):

	def __init__(self):
		self.name = "L.A.R.I."
		self.cards_played = []
		self.hands = dict()
		self.hands[self.name] = []
		self.player_names = []
		self._clear()
		
	def _clear(self):
		"""
		Clear any state.
		"""
		self._score = 0
		self.hands.clear()
		self.hands[self.name] = []
		deck = Deck()
		for p in self.player_names:
			if p != self.name:
				self.hands[p] = deck.get_deck()
		
		self.cards_played = []
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
		return self.hands[self.name]
		
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

	def remove_cards_from_player(self, player, cards):
		"""
		Takes a player name (str), and a list of cards
		Removes the cards from the player's hand
		"""
		for p, h in self.hands.items():
			if p == player:
				for c in cards:
					if c in h:
						h.remove(c)
						
	def add_cards_to_hand(self, cards):
		"""
		Takes a list of two character strings representing cards as an argument
		and returns nothing.
		This list can be any length.
		"""
		self.hands[self.name].extend(cards)
		for p in self.player_names:
			if p != self.name:
				self.remove_cards_from_player(p, cards)
								
	def play_card(self, lead, trick):
		# If we have a 2C, play it (as it should always be played first).
		try:
			idx = self.hands[self.name].index('2C')
			card = self.hands[self.name].pop(idx)
			return card
		except ValueError:
			pass

		player_order = order_players(self.player_names, lead)
		idx = player_order.index(self.name)	
			
		#remove the cards played in the trick from all player's hands
		for p in self.player_names:
			if p != self.name:
				self.remove_cards_from_player(p, trick)
			
		if DEBUG_JR: 
			for p in self.player_names:
				print("PLAYER ",p," HAND: ", self.hands[p])

		# TODO: Thoughts on adding hard coded rules here?
		#   - If we're last to play, play the lowest card that can win
		#   - Play Ace of Spades if we have it
		player_order = order_players(self.player_names, lead)
		idx = player_order.index(self.name)
		best_plays = []
		if DEBUG_JR: print("--------------_ENTERING THE MONTE CARLO ZONE----------------")

		root_state = SpadesState(self.name, player_order, trick, self.hands, copy(self.tricks_won))

		_mcts = mcts(timeLimit=MCTS_SEARCH_TIME)
		best_action = _mcts.search(initialState=root_state)

		if DEBUG_JR: print("BEST ACTION:", best_action[idx])
		
		return best_action[idx]


	def collect_trick(self, lead, winner, trick):
		# Update which cards have been played
		self.cards_played = self.cards_played + trick

		# Update information about opponent hands (if possible).
		player_order = order_players(self.player_names, lead)
		lead_suit = get_suit(trick[0])
		for idx, c in enumerate(trick[1:]):
			if get_suit(c) != lead_suit:
				# AHA! They no longer have any cards of lead_suit.
				if DEBUG_JR: print(self.player_names[idx], " out of suit ", lead_suit)
				self.remove_cards_from_player(idx, get_all_cards_suit(lead_suit))
				
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

