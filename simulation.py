import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import numpy as np
import requests
import pylab
import pandas as pd

'''
Variables
'''
player_list = ['Player 1', 'Player 2']
rounds = 10
stores = 1
locations = ['store', 'junkyard', 'pawn shop', 'hospital', 'pharmacy']
for player in player_list:
    locations.append(f'{player}\'s home'.lower())
    locations.append(f'{player}\'s workplace'.lower())
verbose = True

player_hp = 5
player_actions = 1
player_starting_currency = 0
player_starting_resources = 0


class Board:
    """
    Track the board state
    """

    def __init__(self):
        self.set_locations = []
        self.locations = locations
        self.layout = None

    def create_board(self):
        """
        Create the game board
        """
        # Build a randomized game board
        G = nx.watts_strogatz_graph(20, 4, .3)

        # Set our node and edge attributes
        for node in G.nodes:
            G.nodes[node]['location'] = 'none'
            G.nodes[node]['color'] = 'grey'
            G.nodes[node]['rad'] = 0.1

        for location in self.locations:
            # select a location where nothing has already been placed
            random_node = np.random.choice(np.setdiff1d(list(G.nodes), self.set_locations))
            G.nodes[random_node]['location'] = location
            self.set_locations.append(random_node)

        # Draw our game board
        nx.draw(G, with_labels=True, node_size=1500, pos=nx.spring_layout(G, seed=42))
        plt.title("spring")

        if verbose:
            print(f' Locations generated:\n')
            [print(f'Node: {x}, Attributes: {y}') for x, y in G.nodes(data=True) if y['location'] != 'none']

        return G


class Player:
    """
    Spawn a player
    """

    def __init__(self, name):
        self.name = name
        self.actions = player_actions
        self.health = player_hp
        self.currency = player_starting_currency
        self.resources = player_starting_resources
        self.position_prev = np.nan

    def update_actions(self, change):
        self.actions += change

    def reset_actions(self):
        self.actions = player_actions

    def update_currency(self, change):
        self.currency += change

    def update_resources(self, change):
        self.resources += change

    def set_start_location(self, board_state):
        # select a location where nothing has already been placed
        empty_locations = [x for x, y in board_state.layout.nodes(data=True) if y['location'] != 'none']
        self.position = np.random.choice(np.setdiff1d(list(board_state.layout.nodes), empty_locations))

    def travel(self, board_state):
        self.position_prev = self.position
        self.position = np.random.choice(list(board_state.layout.neighbors(self.position)))
        print(f'{self.name} moved from {self.position_prev} to {self.position}')

    def trigger_location_effects(self, board_state):
        if board_state.layout.nodes[self.position]['location'] == f'{self.name}\'s workplace'.lower():
            self.update_currency(5)
        if board_state.layout.nodes[self.position]['location'] == 'junkyard':
            self.update_resources(5)
        if verbose:
            print(f"Current location: {board.layout.nodes[player.position]['location']}")
            print(f"Currency = {self.currency}")
            print(f"Resources = {self.resources}")


'''
Main Loop
'''

# Create Player Objects
players = {name: Player(name=name) for name in player_list}

# Create the Board
board = Board()
board.layout = board.create_board()

# Set the player starting location
for player in players.values():
    player.set_start_location(board)

# Initialize the game

## for each round
for round in range(0, rounds):
    print(f'\n\n---Round {round}---')

    # each player will take their turn
    for player in players.values():
        for action in range(0, player_actions):
            print(f'\n---{player.name}: Action {action}---')
            while player.actions > 0:
                player.travel(board)
                player.trigger_location_effects(board)
                player.update_actions(-1)
        player.reset_actions()
