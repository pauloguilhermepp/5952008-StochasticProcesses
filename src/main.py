import csv
import math
from collections import Counter

NUMBER_OF_STATES = 3

def read_csv(file_path):
    data = []

    with open(file_path, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(int(row[0]))

    return data

def calculate_likelihood(data, order):
    sequences = [tuple(data[i:i + order + 1]) for i in range(len(data) - order)]
    frequency = Counter(sequences)
    total = sum(frequency.values())
    probability = {key: count / total for key, count in frequency.items()}

    likelihood = 1
    for i in range(len(data) - order):
        subsequence = tuple(data[i:i + order + 1])
        likelihood *= probability.get(subsequence, 0)

    return likelihood

def calculate_likelihoods(data, orders, verbose=False):
    likelihoods = []

    for order in orders:
        likelihoods.append(calculate_likelihood(data, order))

    if verbose:
        print("Order Likelihood")
        for order in orders[:-1]:
            print(f"{order}     {likelihoods[order]}")

    
    return likelihoods

def calculate_likelihood_ratios(data, orders, verbose=False):
    likelihoods = calculate_likelihoods(data, orders, verbose)
    likelihood_ratios = [likelihoods[i] / likelihoods[-1] for i in orders[:-1]]
    return likelihood_ratios

def calculate_aic(data, orders, verbose=False):
    k = orders[-1]
    likelihood_ratios = calculate_likelihood_ratios(data, orders, verbose)
    eta = [-2 * math.log(likelihood_ratio) for likelihood_ratio in likelihood_ratios]
    aic = [eta[i] - 2 * (NUMBER_OF_STATES**k - NUMBER_OF_STATES**i) * (NUMBER_OF_STATES - 1) for i in orders[:-1]]
    return aic

def calculate_metrics(data, orders, verbose=False):
    aic = calculate_aic(data, orders, verbose)
    print(aic)

def main():
    max_possible_order = 2
    possible_orders = [i for i in range(0, max_possible_order + 2)]
    data = read_csv("data/group01.csv")
    calculate_metrics(data, possible_orders, True)

if __name__ == "__main__":
    main()
