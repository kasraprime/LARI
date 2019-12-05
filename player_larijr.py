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
		self.name = "L.A.R.I Jr" + str(random.randint(1,9999999))
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