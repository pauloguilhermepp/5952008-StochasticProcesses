import sys
import csv
import random


class MarkovChain:
    def __init__(self, prob_matrix):
        self.prob_matrix = prob_matrix
        self.order = self.get_order(prob_matrix)

    def get_order(self, matrix):
        if isinstance(matrix, list):
            return 1 + self.get_order(matrix[0])
        return -1

    def get_next_state_probs(self, previous_states):
        if self.order == 0:
            previous_states = []
        else:
            previous_states = previous_states[-self.order :]

        element = self.prob_matrix
        for index in previous_states:
            element = element[index]

        return element

    def get_next_state(self, previous_states):
        random_num = random.random()
        probs = self.get_next_state_probs(previous_states)

        index = 0
        for prob in probs:
            random_num -= prob

            if random_num <= 0:
                return index

            index += 1

        print(
            f'WARNING: Impossible to get next state from "{previous_states[-2]}, {previous_states[-1]}"'
        )
        sys.exit(-1)

    def run(self, initial_states, num_new_states, random_seed=42, file_path=None):
        simulation = initial_states

        random.seed(random_seed)

        for _ in range(num_new_states):
            next_state = self.get_next_state(simulation)
            simulation.append(next_state)

        if file_path:
            self.save(simulation, file_path)

        return simulation

    def save(self, simulation, file_path):
        with open(file_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows([[num] for num in simulation])

def main():
    random_seed = 42
    num_exp_per_mc = 4
    prob_matrixes = [
        [0.85, 0.10, 0.05],
        [[0.85, 0.10, 0.05], [0.02, 0.97, 0.01], [0.07, 0.01, 0.92]],
        [[[0.85, 0.10, 0.05], [0.02, 0.97, 0.01], [0.07, 0.01, 0.92]],
         [[0.03, 0.95, 0.02], [0.08, 0.03, 0.89], [0.80, 0.15, 0.05]],
         [[0.08, 0.02, 0.90], [0.97, 0.01, 0.02], [0.04, 0.93, 0.03]],]
    ]

    random.seed(random_seed)

    for idx, prob_matrix in enumerate(prob_matrixes):
        mc = MarkovChain(prob_matrix)

        for experiment in range(0, num_exp_per_mc):
            mc.run(
                initial_states=[2, 1],
                num_new_states=100,
                random_seed=random.randint(0, 10**5),
                file_path=f"data/labeled/order{idx}/ex{experiment}.csv",
            )

if __name__ == "__main__":
    main()