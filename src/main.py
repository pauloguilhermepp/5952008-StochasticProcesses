from MarkovChainEstimator import MarkovChainEstimator


def main():
    mce = MarkovChainEstimator()
    mce.run(data_path="data/labeled/order2/ex2.csv", max_possible_order=2, verbose=True)


if __name__ == "__main__":
    main()
