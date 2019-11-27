
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