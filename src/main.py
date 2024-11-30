import csv
from collections import Counter

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
    likelihoods = {}

    for order in orders:
        likelihoods[order] = calculate_likelihood(data, order)

    if verbose:
        print("Order Likelihood")
        for order in orders:
            print(f"{order}     {likelihoods[order]}")

    
    return likelihoods

def main():
    possible_orders = [0, 1, 2]
    data = read_csv("data/group01.csv")
    calculate_likelihoods(data, possible_orders, verbose=True)

if __name__ == "__main__":
    main()
