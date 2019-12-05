import random
import operator
from copy import copy
from spades_state import SpadesState
from mcts import mcts
from util import *

MCTS_SEARCH_TIME = 1200
NUM_SIMS = 5
DEBUG_JR = False

class Player(object):
	"""
	Project Player interface.
	"""
	def __init__(self):
		self.name = "Random LARI" + str(random.randint(1,9999999))
		self._clear()

		
	def _clear(self):
		"""
		Clear any state.
		"""
		self._score = 0
		self.hand = []
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

	def score(self):
		"""
		Calculates and returns the score for the game being played.
		"""
		return self._score