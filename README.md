# Titled Tuesday Analysis

## Introduction
On September 14th, the esteemed Csquared Podcast, anchored by Grandmasters Fabiano Caruana and Cristian Chirila, played host to the legendary former World Chess Champion, Vladimir Kramnik. The session delved deep into the pressing concern of online Chess cheating. Over two engrossing hours, Kramnik pulled no punches, stating that online cheating in chess has become rampant. He even went so far as to suggest that he is disproportionately targeted, alleging that Chess.com doesn't scrutinize games involving him as rigorously as they do for other luminaries like Hikaru Nakamura or Magnus Carlsen.

## Data Collection
Our analysis is underpinned by data gleaned directly from the Chess.com API. Though the API isn’t publicized, it still presents a straightforward avenue to harvest all the games from Titled Tuesday. As of September 19th, our dataset boasts 141,449 games from 2023, complemented by 75,737 unique matches from the previous year, 2022.

## The Analysis
To ensure robustness in our findings, every game in our dataset is rigorously assessed using Stockfish 16. Each move within a game is evaluated for a span of one second, after which the results are cataloged. These computed moves are then juxtaposed with the actual moves executed during the game.

## Other Resources
### Opening Tree
I built an opening tree for the Chess.com Titled Tuesday games based on all games. The Tree is pickled as 'opening_tree.pkl'. To retrieve the number of moves for an opening use:

```python
fools_mate_moves = [
    {'from': 'f2', 'to': 'f3'},
    {'from': 'e7', 'to': 'e5'},
    {'from': 'g2', 'to': 'g4'},
    {'from': 'd8', 'to': 'h4'},
]
move_counts_from_graph(sicilian,opening_tree)
{'f2->f3': {'count': 60, 'rank': 18}, 'e7->e5': {'count': 17, 'rank': 2}, 'g2->g4': {'count': 1, 'rank': 5}, 'd8->h4': {'count': 1, 'rank': 1}}
```

### ELO Prediction
Furthermore, multiple sources have stated that it is impossible to predict the ELO of a player based on the moves of one game. While I agree with the assertion that there is little signal in looking at a singular game, previous endevours have failed to take into consideration the sequential nature of a game. I fit an LSTM with the following variables: time per move, Evalutation of the real move, Evaluation of the best move, Colour of the Player, and the remaining time for the whole game. The model training procedure can be found in 03_LSTM_ELO_Prediction.ipynb. The folder '../Model' contains an initial trained on 6700 games that predicts the ELO of a player with an Mean Absolute Error of ~190 Elo points.  

## Forthcoming
I will fact-check the claims by the great Kramnik and see if there is any truth to them. This project will *not* be a witch-hunt. I am not interested in finding cheaters, but rather in finding out if there is any truth to the claims made by Kramnik.