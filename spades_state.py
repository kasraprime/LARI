import itertools
import operator
import random
from collections import deque
from copy import deepcopy
from card_helpers import get_rank, get_suit, get_all_cards_suit

class SpadesState:
    def __init__(self, player, players, trick, hands, score_hand, score_total, played):
        #our player name
        self.player = player
        #list of playes in order of play
        self.players = players
        #current trick in order of play
        self.trick = trick
        #dictionary of all players hands
        self.hands = hands
        #dict of score for each hands
        self.score_hand = score_hand
        #dict of score for the total game
        self.score_total = score_total
        #list of played cards
        self.played = played

    #get random cards for rest of players not already played
    #return all finished tricks
    def getPossibleActions(self):
        s = []
        i = 0
        for t in self.trick:
            s.append([t])
            i = i + 1

        for j in range(i,len(self.players)):
            if len(self.trick) == 0:
                 valid_cards = self.hands[self.players[j]]
            else:
                cards = self.hands[self.players[j]]
                lead_suit = get_suit(self.trick[0])
                valid_cards = list(set(cards).intersection(get_all_cards_suit(lead_suit)))
                if len(valid_cards) == 0:
                    valid_cards = self.hands[self.players[j]]

            s.append(valid_cards)

        actions = list(itertools.product(*s))

        return actions

    def takeAction(self, action):
        new_state = deepcopy(self)

        #remove cards from action (finished trick) from all players hands
        for c in action:
            for p in self.players:
                if c in new_state.hands[p]:
                    new_state.hands[p].remove(c)

        #calculate resulting hand, use action( finished trick )
        lead_suit = action[0][1:]
        max_rank = 0
        winning_player_indx = 0
        for i, c in enumerate(action):
            if c[1:] == lead_suit:
                if get_rank(c) > max_rank:
                    winning_player_indx = i

        new_state.score_hand[self.players[winning_player_indx]] += 1

        #put players in order if new hand
        new_state.players = deque(self.players)
        new_state.players.rotate(-winning_player_indx)
        new_state.players = list(new_state.players)

        #generate trick, pick random cards for other players up to player
        new_state.trick = []
        for p in new_state.players:
            if p == self.player:
                break
            c = random.choice(self.hands[p])
            new_state.trick.append(c)
            if c in new_state.hands[p]:
                new_state.hands[p].remove(c)

        #add cards from action (finished trick) and trick from all hands
        new_state.played.append(new_state.trick)
        new_state.played.append(action)

        return new_state

    def isTerminal(self):
        terminal = False
        if len(self.played) == 52:
            terminal = True

        if len(self.hands[self.players[0]]) == 0:
            terminal = True
        if len(self.hands[self.players[1]]) == 0:
            terminal = True
        if len(self.hands[self.players[2]]) == 0:
            terminal = True
        if len(self.hands[self.players[3]]) == 0:
            terminal = True

        return terminal

    def getReward(self):
        reward = 0
        
        #get the winning player from the dict of scores
        winning_player = max(self.score_hand.items(), key=operator.itemgetter(1))[0]

        if winning_player == self.player:
            reward = 1

        return reward