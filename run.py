import sys
from game_engine import GameEngine
from player_lari import PlayerRandom
from player_lari import PlayerPassiveLARI

WINNING_SCORE = 100

def run():
    args = sys.argv[1:]

    if len(args) != 1:
        print("Usage: run NUM_ITERATIONS")
        return -1

    num_games = args[0]

    try:
        num_games = int(num_games)
    except:
        print("Usage: run NUM_ITERATIONS")
        return -1

    # Create game engine
    gm = GameEngine(WINNING_SCORE)

    # Create players
    player_1 = PlayerPassiveLARI()
    player_2 = PlayerRandom()
    player_3 = PlayerRandom()
    player_4 = PlayerRandom()

    gm.set_players([player_1, player_2, player_3, player_4])

    for game in range(int(num_games)):
        result = gm.play_round()
        print("\n++++++++++++++++++++++++++++++++++ FINAL SCORE ++++++++++++++++++++++++++++++++++++++++++++++++")
        print(result)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        gm.clear()

if __name__ == '__main__':
    run()
