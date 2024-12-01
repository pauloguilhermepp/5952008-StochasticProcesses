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

def calculate_likelihoods(data, orders):
    likelihoods = []

    for order in orders:
        likelihoods.append(calculate_likelihood(data, order))
    
    return likelihoods

def calculate_likelihood_ratios(data, orders, return_likelihood=False):
    likelihoods = calculate_likelihoods(data, orders)
    likelihood_ratios = [likelihoods[i] / likelihoods[-1] for i in orders[:-1]]

    if return_likelihood:
        return likelihood_ratios, likelihoods[:-1]

    return likelihood_ratios

def calculate_aic(eta, k):
    aic = [eta[i] - 2 * (NUMBER_OF_STATES**k - NUMBER_OF_STATES**i) * (NUMBER_OF_STATES - 1) for i in range(0, k)]
    best_aic = aic.index(min(aic))
    return (aic, best_aic)

def calculate_bic(eta, k, sample_size):
    bic = [eta[i] - (NUMBER_OF_STATES**k - NUMBER_OF_STATES**i) * (NUMBER_OF_STATES - 1) * sample_size for i in range(0, k)]
    best_bic = bic.index(min(bic))
    return (bic, best_bic)


def calculate_metrics(data, orders, verbose=False):
    k = orders[-1]
    sample_size = len(data)
    likelihood_ratios, likelihoods = calculate_likelihood_ratios(data, orders, return_likelihood=True)
    eta = [-2 * math.log(likelihood_ratio) for likelihood_ratio in likelihood_ratios]

    aic, best_aic = calculate_aic(eta, k)
    bic, best_bic = calculate_bic(eta, k, sample_size)

    if verbose:
        print("Order \t Likelihoods \t Lhd Ratios \t AIC \t\t BIC")
        for order in orders[:-1]:
            print(f"{order} \t {likelihoods[order]:.3e} \t {likelihood_ratios[order]:.3e} \t {aic[order]:.3e} \t {bic[order]:.3e}")
        
        print(f"\nBest AIC Solution: Order {best_aic}")
        print(f"Best BIC Solution: Order {best_bic}")


def main():
    max_possible_order = 2
    possible_orders = [i for i in range(0, max_possible_order + 2)]
    data = read_csv("data/labeled/order0/ex1.csv")
    calculate_metrics(data, possible_orders, True)

if __name__ == "__main__":
    main()
