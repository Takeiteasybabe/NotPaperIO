from typing import Tuple

import numpy as np

from game import LocalGame


BASE_BOARD_DIMENSION = 31 * 30 // 5


def convert_coordinates(coordinates: Tuple[int, int]) -> Tuple[int, int]:
    return ((coordinates[0] - 15) // 30, (coordinates[1] - 15) // 30)


def reconstruct_board(game: LocalGame, player_num: int = 1) -> np.ndarray:
    """
    Reconstructs board as matrix from current game state

    Args:
        game: Game instance
        player_num: Your player id

    Returns:
        Board as numpy array. 
        Shape: BASE_BOARD_DIMENSION x BASE_BOARD_DIMENSION
        Legend:
            0 - neutral territory
            1 - your player
            2 - your territory
            3 - your trace
            -1 - enemy players
            -2 - enemy territory
            -3 - enemy trace
            10 - saw
            11 - accelerator
            12 - deaccelerator
    """
    board = np.zeros((BASE_BOARD_DIMENSION, BASE_BOARD_DIMENSION))
    game_log = game.game_log[1]

    # Priority: player position > bonus > line > territory
    players = game_log['players']
    # bonuses = game_log['bonuses']  No bonuses in baseline

    # Many loops because of priorities
    for player in players:
        data = players[player]
        territory = data['territory']
        for elem in territory:
            normalized_coordinates = convert_coordinates(elem)
            # This can be sped up by vectorizing
            board[normalized_coordinates] = -4 * int(player != player_num) + 2

    for player in players:
        data = players[player]
        lines = data['lines']
        for elem in lines:
            normalized_coordinates = convert_coordinates(elem)
            board[normalized_coordinates] = -6 * int(player != player_num) + 3

    for player in players:
        data = players[player]
        position = data['position']
        normalized_coordinates = convert_coordinates(position)
        board[normalized_coordinates] = -2 * int(player != player_num) + 1

    return board
