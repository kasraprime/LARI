import random
from collections import deque
from copy import copy
from util import *

ROUND_DEBUG = True
HAND_DEBUG = True
TRICK_DEBUG = True

TRUMP = False

class GameEngine(object):

    def __init__(self, winning_score):
        self.winning_score = winning_score
        self.players = []
        self.player_names = []
        self.player_scores = [0, 0, 0, 0]
        self.deck = Deck()
        pass

    def set_players(self, players):
        """
        Players should be given in clockwise order.
        """
        self.players = players
        self.player_names = list(map(lambda p: p.get_name(), players))

    def clear(self):
        self.player_scores = [0, 0, 0, 0]

    def play_round(self):
        """
        Play one round. Rounds consist of multiple hands.
        """
        num_winners = 0
        while num_winners != 1:
            # Play Hand.
            self.play_hand()

            # Update Scores.
            if ROUND_DEBUG: print("\n___________CURRENT_SCORE___________________________")

            for idx, p in enumerate(self.players):
                self.player_scores[idx] = self.player_scores[idx] + p.score()
                if ROUND_DEBUG: print(p.get_name() + " => " + str(self.player_scores[idx]))


            # Check if the game should end
            num_winners = 0
            for ps in self.player_scores:
                if ps >= self.winning_score:
                    num_winners = num_winners + 1

        # Sort players by score
        unsorted_scoreboard = zip(self.player_scores, self.player_names)
        sorted_scoreboard = sorted(unsorted_scoreboard, key=lambda s: s[0], reverse=True)
        return sorted_scoreboard

    def play_hand(self):
        """
        Play one hand. Hands consist of 13 tricks.
        """
        # Shuffle & split deck.
        self.deck.shuffle()
        hands = self.deck.deal()

        # Clear player hands.
        for p in self.players:
            p.new_hand(self.player_names)

        # Deal hands to players.
        start_idx = -1
        for idx, p in enumerate(self.players):
            # Find who starts.
            if "2C" in hands[idx]:
                start_idx = idx
            p.add_cards_to_hand(hands[idx])

        if HAND_DEBUG:
            print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~Player Hands~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            for p in self.players:
                print(p.get_name())
                print(p.get_hand())

        # Order players based on who starts.
        ordered_players = deque(self.players)
        ordered_players.rotate(-start_idx)
        ordered_players = list(ordered_players)

        for i in range(0,13):
            winner = self.play_trick(ordered_players)
            win_idx = self.player_names.index(winner)
            
            # Rotate the ordering so the winner gets to start.
            ordered_players = deque(self.players)
            ordered_players.rotate(-win_idx)
            ordered_players = list(ordered_players)

    def play_trick(self, ordered_players):
        """
        Play a trick and return the name of the winner.
        """
        lead_player = ordered_players[0].get_name()

        if TRICK_DEBUG: print("\n----------------------------------\nLead Trick Player: " + lead_player)

        trick = []
        for o_p in ordered_players:
            card_played = o_p.play_card(lead_player, trick)
            trick.append(card_played)
            if TRICK_DEBUG: print("\t " + o_p.get_name() + " played: " + card_played)

        winner_idx = self.trick_winner(trick)
        winner = ordered_players[winner_idx].get_name()

        if TRICK_DEBUG: print("Trick Winner: " + winner)

        for p in self.players:
            p.collect_trick(lead_player, winner, trick)

        if TRICK_DEBUG:
            print("Trick Scores:")
            for p in self.players:
                print("\t" + p.get_name() + " => " + str(p.get_tricks_won()))
            print("---------------------------------")

        return winner
        
    def trick_winner(self, trick):
        """
        Determines the index of the card that won the trick.
        """
        winning_card = trick[0]
        winning_idx = 0
        for idx, c in enumerate(trick[1:]):
            winning_card = self.deck.compare_cards(winning_card, c)
            if winning_card == c:
                winning_idx = idx + 1
        return winning_idx
