#!/usr/bin/env python

'''
These objects and functions are part of a larger poker assistant project.
Content of this script enable the user to simulate game of Texas Holdem Poker.
'''

__author__ = 'François-Guillaume Fernandez'
__license__ = 'MIT License'
__version__ = '0.1'
__maintainer__ = 'François-Guillaume Fernandez'
__status__ = 'Development'

from game import Player, Game, get_hand_value, get_winners


def main():
    players = [Player() for k in range(4)]
    g = Game(players)
    g.deal()
    g.hit()
    g.hit()
    g.hit()
    hands = []
    for k in range(4):
        print('Player %s: %s' % (k, g.get_player_cards(k)))
        hands.append(get_hand_value(g.community_cards + g.players[k].cards))
        print(hands[-1])
    print('Winner:', get_winners(hands))


if __name__ == "__main__":
    main()
