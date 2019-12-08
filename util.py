from collections import deque
from copy import copy
import operator
import random


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

def get_player_score(tricks_won, player_name):
	# Sort players from highest to lowest number of tricks won
	sorted_tricks_won = sorted(tricks_won.items(), key=operator.itemgetter(1), reverse=True)
	our_place = list(map(lambda x: x[0], sorted_tricks_won)).index(player_name)
	# Get places.
	first_place_name = sorted_tricks_won[0][0]
	second_place_name = sorted_tricks_won[1][0]
	third_place_name = sorted_tricks_won[2][0]
	fourth_place_name = sorted_tricks_won[3][0]

	if tricks_won[first_place_name] == tricks_won[second_place_name]: # Tie
		if tricks_won[second_place_name] == tricks_won[third_place_name]: # Three way tie
			if our_place < 3: # We tied with two others.
				return 3
		else:
			if our_place < 2: # We tied with someone else.
				return 5
	else: # Single winner
		if our_place < 1: # We won!
			return 11

	return 0

def order_players(clockwise_players, lead_player):
	idx = clockwise_players.index(lead_player)
	ordered_players = deque(clockwise_players)
	ordered_players.rotate(-idx)
	return list(ordered_players)


class Deck():
	"""
	Deck of cards.
	"""
	def __init__(self):
		deck = []
		for s in self.get_suits():
			for r in self.get_ranks():
				deck.append(r+s)
		self.deck = deck

	def shuffle(self):
		random.shuffle(self.deck)

	def remove_cards(self, cards):
		self.deck = list(set(self.deck) - set(cards))

	def compare_cards(self, a, b):
		a_suit = a[-1:]
		a_rank_val = self.get_rank_value(a[0:-1])
		b_suit = b[-1:]
		b_rank_val = self.get_rank_value(b[0:-1])

		if a_suit == b_suit: 
			return a if a_rank_val > b_rank_val else b
		else:
			return a

	def get_rank_value(self, r):
		"""
		this function gives the value (strength) of each card
		"""
		if r == 'A':
			return 14
		elif r == 'K':
			return 13
		elif r == 'Q':
			return 12
		elif r == 'J':
			return 11
		elif r == 'T':
			return 10
		else:
			return int(r)

	def deal(self):
		"""
		Split deck into 4 equal hands.
		"""
		hands = []
		hands.append(self.deck[0:13])
		hands.append(self.deck[13:26])
		hands.append(self.deck[26:39])
		hands.append(self.deck[39:52])
		return hands

	def get_deck(self):
		return self.deck
		
	def get_suits(self):
		return ["S", "H", "D", "C"]

	def get_ranks(self):
		return ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

	def __str__(self):
		return str(self.deck)
