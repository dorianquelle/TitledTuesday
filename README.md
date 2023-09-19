# Titled Tuesday Analysis

## Introduction
On September 14th, the esteemed Csquared Podcast, anchored by Grandmasters Fabiano Caruana and Cristian Chirila, played host to the legendary former World Chess Champion, Vladimir Kramnik. The session delved deep into the pressing concern of online Chess cheating. Over two engrossing hours, Kramnik pulled no punches, stating that online cheating in chess has become rampant. He even went so far as to suggest that he is disproportionately targeted, alleging that Chess.com doesn't scrutinize games involving him as rigorously as they do for other luminaries like Hikaru Nakamura or Magnus Carlsen.

## Data Collection
Our analysis is underpinned by data gleaned directly from the Chess.com API. Though the API isn’t publicized, it still presents a straightforward avenue to harvest all the games from Titled Tuesday. As of September 19th, our dataset boasts 141,449 games from 2023, complemented by 75,737 unique matches from the previous year, 2022.

## The Analysis
To ensure robustness in our findings, every game in our dataset is rigorously assessed using Stockfish 16. Each move within a game is evaluated for a span of one second, after which the results are cataloged. These computed moves are then juxtaposed with the actual moves executed during the game.

## Forthcoming
I will fact-check the claims by the great Kramnik and see if there is any truth to them. This project will *not* be a witch-hunt. I am not interested in finding cheaters, but rather in finding out if there is any truth to the claims made by Kramnik.