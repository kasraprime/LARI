import itertools
import operator
import random
from collections import deque
from copy import deepcopy
from util import *

MAX_BRANCH = 5
DEBUG = False

class SpadesState:
	def __init__(self, player, players, trick, hands, tricks_won):
		#our player name
		self.player = player
		#list of playes in order of play
		self.players = players
		#current trick in order of play. (Will only be used on root node).
		self.trick = trick
		#dictionary of all players hands
		self.hands = hands
		#dict of player_name => tricks_won: number of tricks won by each player in one hand
		self.tricks_won = tricks_won

	#get random cards for rest of players not already played (including our player)
	#return all finished tricks
	def getPossibleActions(self):
		s = []
		i = 0
		# Adds cards that have been played in this trick to to the new state.
		for t in self.trick:
			s.append([t])
			i = i + 1

		# Loop through all players that haven't yet participated in the current trick.
		for j in range(i, len(self.players)):
			if len(self.trick) == 0:
				# First person playing can play any card.
				valid_cards = self.hands[self.players[j]]
			else:
				# playing the leading suit if possible
				cards = self.hands[self.players[j]]
				lead_suit = get_suit(self.trick[0])
				valid_cards = list(set(cards).intersection(get_all_cards_suit(lead_suit)))
				if len(valid_cards) == 0:
					# Play any card if the leading suit is not in hand
					valid_cards = self.hands[self.players[j]]

			# Cap number of branches.
			#random.shuffle(valid_cards)
			#s.append(valid_cards[:MAX_BRANCH])
			s.append(valid_cards)
			
		# Cartesian product of all players' possible plays.
		actions = list(itertools.product(*s))
		
		if DEBUG: print("STATE:", self.hands)
		if DEBUG: print("POSSIBLE ACTIONS:", actions)
		
		return actions

	def takeAction(self, action):
		new_state = deepcopy(self)
		new_state.trick = []

		#remove cards from action (finished trick) from all players hands
		for c in action:
			for p in self.players:
				if c in new_state.hands[p]:
					new_state.hands[p].remove(c)

		#calculate resulting hand, use action( finished trick ), and find the winner of current trick
		lead_suit = get_suit(action[0])
		max_rank = get_rank(action[0])
		winning_player_indx = 0
		# TODO: for the next phase we should consider braking with spades as well
		for i, c in enumerate(action):
			if get_suit(c) == lead_suit and get_rank(c) > max_rank:
				max_rank = get_rank(c)
				winning_player_indx = i

		# Give the trick to the winning player.
		new_state.tricks_won[self.players[winning_player_indx]] += 1

		#put players in order if new hand
		new_state.players = deque(self.players)
		new_state.players.rotate(-winning_player_indx)
		new_state.players = list(new_state.players)

		if DEBUG: print("ACTION TAKEN" + str(action))

		return new_state

	def isTerminal(self):
		return sum(self.tricks_won.values()) == 13

	def getReward(self):
	   return get_player_score(self.tricks_won, self.player) 
