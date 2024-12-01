import csv
import math
from collections import Counter


class MarkovChainEstimator:
    def __init__(self):
        pass

    def read_csv(self, file_path):
        data = []

        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(int(row[0]))

        return data

    def calculate_log_likelihood(self, data, order):
        self.__num_states = len(set(data))

        sequences = [tuple(data[i : i + order + 1]) for i in range(len(data) - order)]
        frequency = Counter(sequences)

        contexts = [tuple(data[i : i + order]) for i in range(len(data) - order)]
        context_frequency = Counter(contexts)

        probability = {
            key: count / context_frequency[key[:-1]] for key, count in frequency.items()
        }

        log_likelihood = 0
        for i in range(len(data) - order):
            subsequence = tuple(data[i : i + order + 1])
            log_likelihood += math.log(probability.get(subsequence))

        return log_likelihood

    def calculate_log_likelihoods(self, data, orders):
        log_likelihoods = []

        for order in orders:
            log_likelihoods.append(self.calculate_log_likelihood(data, order))

        return log_likelihoods

    def calculate_log_likelihood_ratio(self, data, orders, return_log_likelihood=False):
        log_likelihoods = self.calculate_log_likelihoods(data, orders)
        log_likelihood_ratio = [
            log_likelihoods[i] - log_likelihoods[-1] for i in orders[:-1]
        ]

        if return_log_likelihood:
            return log_likelihood_ratio, log_likelihoods[:-1]

        return log_likelihood_ratio

    def calculate_aic(self, eta, k):
        aic = [
            eta[i]
            - 2
            * (self.__num_states**k - self.__num_states**i)
            * (self.__num_states - 1)
            for i in range(0, k)
        ]
        best_aic = aic.index(min(aic))
        return (aic, best_aic)

    def calculate_bic(self, eta, k, sample_size):
        bic = [
            eta[i]
            - (self.__num_states**k - self.__num_states**i)
            * (self.__num_states - 1)
            * math.log(sample_size)
            for i in range(0, k)
        ]
        best_bic = bic.index(min(bic))
        return (bic, best_bic)

    def run(self, data_path, max_possible_order, verbose=False):
        orders = [i for i in range(0, max_possible_order + 2)]
        data = self.read_csv(data_path)

        k = orders[-1]
        sample_size = len(data)

        log_likelihood_ratio, log_likelihoods = self.calculate_log_likelihood_ratio(
            data, orders, return_log_likelihood=True
        )
        eta = [
            -2 * log_likelihood_ratio for log_likelihood_ratio in log_likelihood_ratio
        ]

        aic, best_aic = self.calculate_aic(eta, k)
        bic, best_bic = self.calculate_bic(eta, k, sample_size)

        if verbose:
            print("Order \t Log Lhd \t Log Lhd Rat \t AIC \t\t BIC")
            for order in orders[:-1]:
                print(
                    f"{order} \t {log_likelihoods[order]:.3e} \t {log_likelihood_ratio[order]:.3e} \t {aic[order]:.3e} \t {bic[order]:.3e}"
                )

            print(f"\nBest AIC Solution: Order {best_aic}")
            print(f"Best BIC Solution: Order {best_bic}")
