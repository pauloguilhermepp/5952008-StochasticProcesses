import os
from MarkovChainEstimator import MarkovChainEstimator


def test_labeled_data():
    orders = [0, 1, 2]
    path = "data/labeled/order"
    mce = MarkovChainEstimator()

    for order in orders:
        csv_dir = f"{path}{order}"
        experiments = os.listdir(f"{path}{order}")

        for experiment in experiments:
            print(f"CSV Path: {csv_dir}/{experiment}")
            mce.run(
                data_path=f"{csv_dir}/{experiment}", max_possible_order=2, verbose=True
            )
            print(100 * "-")


def test_professor_data():
    groups = [1, 2, 3]
    path = "data/professor"
    mce = MarkovChainEstimator()

    for group in groups:
        csv_path = f"{path}/group0{group}.csv"
        print(f"CSV Path: {csv_path}")
        mce.run(data_path=csv_path, max_possible_order=2, verbose=True)
        print(100 * "-")


def main():
    test_labeled_data()
    test_professor_data()


if __name__ == "__main__":
    main()
