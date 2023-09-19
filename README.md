# Titled Tuesday Analysis

## Introduction
On the 14th of September the Csquared Podcast hosted by Grandmasters Fabiano Caruana and Cristian Chirila, invited former World Champion Vladimir Kramnik to opine on the state of online Chess cheating. 

In the two hour interview Kramnik claims that cheating online is rampant, with swaths of players cheating. He further alleges that he is a particular target of cheating as Chess.com does not check games against him to the same extent as against Hikaru or Carlsen. 

## The Data
The data used in this analysis was scraped from the Chess.com API. While the API is not documented, it is quite easy to extract all Titled Tuesday Games. On the 19th of September we currently have downloaded 141.449 games for 2023 and 75.737 unique games for the year 2022. 

## The Analysis
I am running Stockfish 16 for each game. Each move is evaluated for one second and the results are stored. The results are then compared to the actual move played.

## Forthcoming
I will fact-check the claims by the great Kramnik and see if there is any truth to them. This project will *not* be a witch-hunt. I am not interested in finding cheaters, but rather in finding out if there is any truth to the claims made by Kramnik.