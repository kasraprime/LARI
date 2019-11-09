import random
from collections import deque

ROUND_DEBUG = False
HAND_DEBUG = False

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
        is_tied = True
        someone_won = False

        while not someone_won or is_tied:
            # Play Hand.
            self.play_hand()

            if ROUND_DEBUG:
                print("HAND SCORES:")
                for p in self.players:
                    print(p.get_name() + " => " + str(p.score()))
                print("============================================\n")
            
            # Update Scores.
            for idx, p in enumerate(self.players):
                self.player_scores[idx] = self.player_scores[idx] + p.score()

            # Check if the game should end
            non_zero_scores = list(filter(lambda x: x > 0, self.player_scores))
            is_tied = len(non_zero_scores) > len(set(non_zero_scores))
            someone_won = any(map(lambda ps: ps >= self.winning_score, self.player_scores))

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

        if HAND_DEBUG:
            print("Hands that will be dealt:")
            print(hands)
            print("=========================================================================\n")

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
            print("Player hands:")
            for p in self.players:
                print(p.get_name())
                print(p.get_hand())
                print("\n")
            print("=========================================================================\n")

        # Order players based on who starts.
        ordered_players = deque(self.players)
        ordered_players.rotate(-start_idx)
        ordered_players = list(ordered_players)

        for i in range(0,13):
            winner = self.play_trick(ordered_players)

            if HAND_DEBUG:
                print("Winner of round " + str(i) + " ==> " + winner)
                print("=========================================================================\n")

            win_idx = -1
            for idx, p in enumerate(self.players):
                if p.get_name == winner:
                    win_idx = idx

            ordered_players = deque(self.players)
            ordered_players.rotate(-win_idx)
            ordered_players = list(ordered_players)

    def play_trick(self, ordered_players):
        """
        Play a trick and return the name of the winner.
        """
        lead_player = ordered_players[0].get_name()
        trick = []
        for o_p in ordered_players:
            card_played = o_p.play_card(lead_player, trick)
            trick.append(card_played)

        winner_idx = self.trick_winner(trick)
        winner = ordered_players[winner_idx].get_name()

        for p in self.players:
            p.collect_trick(lead_player, winner, trick)

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

    def compare_cards(self, a, b):
        a_suit = a[-1:]
        a_rank_val = self.get_rank_value(a[0:-1])
        b_suit = b[-1:]
        b_rank_val = self.get_rank_value(b[0:-1])

        if a_suit == 'S':
            if b_suit == 'S':
                return a if a_rank_val > b_rank_val else b
            else:
                return a
        else:
            if b_suit == 'S':
                return b
            elif a_suit == b_suit:
                return a if a_rank_val > b_rank_val else b
            else:
                return a

    def get_rank_value(self, r):
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

    def get_suits(self):
        return ["S", "H", "D", "C"]

    def get_ranks(self):
        return ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]

    def __str__(self):
        return str(self.deck)
