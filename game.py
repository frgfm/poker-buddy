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

import numpy as np


def get_card_value(idx):
    return [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A'][idx]


class Card:

    def __init__(self, suit, value):
        self.suit = suit  # Diamonds, Clubs, Hearts, Spades
        self.value = value  # 1 -> 13

    def get_value(self):
        return get_card_value(self.value)

    def get_name(self):
        return '%s %s' % (self.get_value(), self.suit)


def get_hand_value(cards):

    # Order the cards
    cards_values = [card.value for card in cards]
    sorted_idx = np.argsort(cards_values)[::-1]
    ordered_cards = np.array(cards)[sorted_idx]
    cards_values = [card.value for card in ordered_cards]
    cards_suits = [card.suit for card in ordered_cards]

    nb_cards = len(cards)

    # Get the occurrences
    from collections import Counter
    suit_count = Counter(cards_suits)
    value_count = Counter(cards_values)

    hand = {'royal flush': None, 'straight flush': None,
            'fours': [], 'full house': None,
            'flush': [], 'straight': [],
            'threes': [], 'double pairs': [], 'pairs': [], 'high': cards_values[0]}

    # Check for straight & flush
    if nb_cards >= 5:
        # Check for flush
        for suit, count in suit_count.items():
            if count >= 5:
                hand['flush'] = [idx for idx, c_suit in enumerate(cards_suits) if c_suit == suit]
                hand['flush'] = suit
                break
        # Check for straight
        if len(value_count.keys()) >= 5:
            flow = 1
            prev_val = cards_values[0]
            tmp_values = cards_values
            # Ace case for straights
            if prev_val == 12:
                tmp_values.append(-1)
            for idx, val in enumerate(tmp_values):
                diff = prev_val - val
                if diff > 0:
                    if diff == 1:
                        flow = flow + 1
                    else:
                        if idx > len(tmp_values) - 5:
                            break
                        flow = 1
                if flow >= 5:
                    hand['straight'].append(val + 4)
                    break
                prev_val = val

    if len(hand['straight']) > 0 and len(hand['flush']) > 0:
        # Straight flush
        flush_suit = cards_suits[hand['flush'][0]]
        for high in hand['straight']:
            # Check if each card is in the flush
            if all(card_idx in hand['flush'] for card_idx, card_value in enumerate(cards_values) if card_value in range(high - 4, high + 1)):
                hand['straight flush'] = (high, flush_suit)

        # Royal flush
        if hand['straight flush'] is not None and hand['straight flush'][0] == 12:
            hand['royal flush'] = hand['straight flush'][1]

    # Check for fours, threes, pairs
    for val, count in value_count.items():
        if count == 4:
            hand['fours'].append(val)
        elif count == 3:
            hand['threes'].append(val)
        elif count == 2:
            hand['pairs'].append(val)

    # Double pairs
    if len(hand['pairs']) >= 2:
        hand['double pairs'] = hand['pairs'][:2]

    # Full House
    if len(hand['threes']) > 0 and len(hand['pairs']) > 0:
        hand['full house'] = (hand['threes'][0], hand['pairs'][0])

    return hand


def get_winners(hands):

    winner_idxs = []

    for hand_type in ['royal flush', 'straight flush', 'fours', 'full house', 'flush', 'straight', 'threes', 'double pairs', 'pairs', 'high']:
        selection = []
        # Short-list hands with current hand type
        for hand_idx, hand in enumerate(hands):
            if isinstance(hand.get(hand_type), list) and len(hand.get(hand_type)) > 0:
                selection.append(hand_idx)
        # print('Checking %s: selection %s' % (hand_type, selection))

        if len(selection) > 0:
            if len(selection) == 1:
                winner_idxs = selection
            else:
                if hand_type == 'royal flush':
                    winner_idxs = selection
                elif hand_type == 'straight flush':
                    flush_high = np.max([hands[idx][hand_type][0] for idx in selection])
                    winner_idxs = [idx for idx in selection if hands[idx][hand_type][0] == flush_high]

                # Case where you need to compare 2 args potentially
                elif hand_type in ['full house', 'double pairs']:
                    shortlist = selection[np.argmax([hands[idx][hand_type][0] for idx in selection])]
                    if isinstance(shortlist, int) or len(shortlist) == 1:
                        winner_idxs = shortlist
                    else:
                        winner_idxs = shortlist[np.argmax([hands[idx][hand_type][1] for idx in shortlist])]

                # All other hand types are comparable with the high card in the hand type
                else:
                    winner_idxs = selection[np.argmax([hands[idx][hand_type][0] for idx in selection])]
            break


    return winner_idxs


class Deck:

    cards = []

    def __init__(self):
        for suit in ['Diamonds', 'Clubs', 'Hearts', 'Spades']:
            for value in range(0, 13):
                self.cards.append(Card(suit, value))

    def drow_card(self):
        import random
        idx = random.randint(0, len(self.cards) - 1)
        card = self.cards[idx]
        del self.cards[idx]

        return card

    def drow_cards(self, nb_cards):
        cards = []
        for c in range(nb_cards):
            cards.append(self.drow_card())
        return cards

class Player:

    cards = []

    def __init__(self):
        self.cash = 1000

    def deal_cards(self, cards):
        self.cards = cards

    def get_cards(self):
        return self.cards


class Game:

    def __init__(self, players):
        self.deck = Deck()
        self.players = players
        self.community_cards = []

    def deal(self):
        print('Dealing cards to players...')
        for p in self.players:
            p.cards = self.deck.drow_cards(2)

    def get_com_cards(self):

        return [card.get_name() for card in self.community_cards]

    def hit(self):
        if len(self.community_cards) == 0:
            self.community_cards = self.deck.drow_cards(3)
            print('Flop:', self.get_com_cards())
        elif len(self.community_cards) == 3:
            self.community_cards.append(self.deck.drow_card())
            print('Turn:', self.get_com_cards())
        elif len(self.community_cards) == 4:
            self.community_cards.append(self.deck.drow_card())
            print('River:', self.get_com_cards())
        else:
            raise ValueError('All community cards are already drown')

    def get_player_cards(self, idx):

        return [card.get_name() for card in self.players[idx].cards]
