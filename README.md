# Poker buddy
This repository hold the different parts of a poker assistant projects. 



## Installation

This project was only developed using Python and numpy.

```
git clone https://github.com/frgfm/poker-buddy.git
cd poker-buddy
pip install requirements.txt
```



## Usage

If you prefer running the simulation directly without entering a shell:

```bash
python src/main.py
```

If you favor using objects in Python, you can use the classes and functions from the game.py file

```python
from game import Player, Game, get_hand_value, get_winners
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
```

Either way, it should simulate a game with an output similar to:
```bash
Dealing cards to players...
Flop: ['6 Hearts', '5 Hearts', '3 Spades']
Turn: ['6 Hearts', '5 Hearts', '3 Spades', 'K Hearts']
River: ['6 Hearts', '5 Hearts', '3 Spades', 'K Hearts', '3 Hearts']
Player 0: ['8 Hearts', '5 Diamonds']
{'royal flush': None, 'straight flush': None, 'fours': [], 'full house': None, 'flush': 'Hearts', 'straight': [], 'threes': [], 'double pairs': [3, 1], 'pairs': [3, 1], 'high': 11}
Player 1: ['4 Spades', 'K Spades']
{'royal flush': None, 'straight flush': None, 'fours': [], 'full house': None, 'flush': [], 'straight': [], 'threes': [], 'double pairs': [11, 1], 'pairs': [11, 1], 'high': 11}
Player 2: ['7 Clubs', '7 Diamonds']
{'royal flush': None, 'straight flush': None, 'fours': [], 'full house': None, 'flush': [], 'straight': [], 'threes': [], 'double pairs': [5, 1], 'pairs': [5, 1], 'high': 11}
Player 3: ['8 Diamonds', '5 Clubs']
{'royal flush': None, 'straight flush': None, 'fours': [], 'full house': None, 'flush': [], 'straight': [], 'threes': [], 'double pairs': [3, 1], 'pairs': [3, 1], 'high': 11}
Winner: 1
```


## TODO
- [x] Model a Texas Holdem Poker game
- [ ] Live computation of odds of winning depending on each player's point of view
- [ ] Investigate card recognition from pictures
- [ ] Investigate Reinforcement Learning to capture player decision-making profile
