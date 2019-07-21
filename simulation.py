import json

from pprint import pprint

from game import LocalGame
from clients import SimplePythonClient
from game_log_parser import reconstruct_board


client = SimplePythonClient()
game = LocalGame([client])

game.send_game_start()
for _ in range(20):
    game.game_loop()
    pprint(game.game_log)
    # with open('log.log', 'a') as f:
    #     json.dump(game.game_log, f)

# Sanity check
board = reconstruct_board(game)
for i in range(-5, 6):
    print(f'{i}: {(board == i).sum()}')