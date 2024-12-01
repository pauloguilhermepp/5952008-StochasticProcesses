# 5952008-StochasticProcesses
## Introduction
This repository contains the project develop in the class *5952008: Stochastic Processes*. Here, both mechanisms to generate simulations or markov chains and estimators to calculate the order of markov chains from data were developed.

## Project Organization
It follows bellow the description of the main parts of this project:
```
root/

├── data
|
|   ├── labeled: Directory with data generated from the *MarkovChain* class with known label.
|
|   ├── professor: Directory with data given from the professor. 
|
├── src
|
|   ├── main.py: File to estimate order of all csv files.
|
|   ├── MarkovChain.py: File used to generate data with known order.
|
|   ├── MarkovChainEstimator: File to estimate the order of a Markov Chain from its simulation.
|
├── results.txt: File with results of main.py with estimated orders of the Markov Chain simulations.
```
