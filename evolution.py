import copy
import random

import numpy as np

from player import Player


class Evolution:
    def __init__(self):
        self.game_mode = "Neuroevolution"

    def q_tournament(self, players: list, Q=16):
        random.shuffle(players)
        return max(players[:Q], key=lambda item: item.fitness)

    def roulette_wheel(self, players: list):
        population_fitness = sum([player.fitness for player in players])
        probabilities = [player.fitness / population_fitness for player in players]
        return np.random.choice(players, p=probabilities)

    def next_population_selection(self, players, num_players):
        """
        Gets list of previous and current players (μ + λ) and returns num_players number of players based on their
        fitness value.

        :param players: list of players in the previous generation
        :param num_players: number of players that we return
        """
        total = 0
        minimum_fitness = 10000
        maximum_fitness = 0
        for i in range(len(players)):
            total += players[i].fitness
            if players[i].fitness < minimum_fitness:
                minimum_fitness = players[i].fitness
            if players[i].fitness > maximum_fitness:
                maximum_fitness = players[i].fitness
        average = total / len(players)
        print(f'Fitness: average {average} | Max: {maximum_fitness} ')
        with open('history.dat', 'a') as file:
            file.write(f'{minimum_fitness} {average} {maximum_fitness} ')
        # # TODO (Implement top-k algorithm here)
        # players.sort(key=lambda x: x.fitness, reverse=True)
        # return players[: num_players]
        # TODO (Additional: Implement Q tournament here)
        winners = []
        for _ in range(num_players):
            winners.append(self.q_tournament(players,Q=8))
        return winners
        # TODO (Additional: Implement roulette wheel here)
        # winners = []
        # for _ in range(num_players):
        #     winners.append(self.roulette_wheel(players))
        # return winners
        # TODO (Additional: Implement SUS here)

        # TODO (Additional: Learning curve)

    def generate_new_population(self, num_players, prev_players=None):
        """
        Gets survivors and returns a list containing num_players number of children.

        :param num_players: Length of returning list
        :param prev_players: List of survivors
        :return: A list of children
        """
        first_generation = prev_players is None
        if first_generation:
            return [Player(self.game_mode) for _ in range(num_players)]
        else:
            # TODO ( Parent selection and child generation )

            new_players = []
            # ## ALL PARENTS METHOD:
            # for i in range(0, len(prev_players), 2):
            #     child_1, child_2 = self.create_children(prev_players[i], prev_players[i + 1])
            #     new_players.extend((child_1, child_2))
            # ## Q TOURNAMENT

            for _ in range(num_players // 2):
                child_1, child_2 = self.create_children(self.q_tournament(prev_players),
                                                        self.q_tournament(prev_players))
                new_players.extend((child_1, child_2))

            # ## ROULETTE WHEEL
            # for _ in range(num_players // 2):
            #    parent_1 = self.roulette_wheel(prev_players)
            #    parent_2 = self.roulette_wheel(prev_players)
            #    child_1, child_2 = self.create_children(parent_1,parent_2)
            #    new_players.extend((child_1, child_2))
            return new_players

    def create_children(self, _first_parent: Player, _second_parent: Player):
        alpha = 0.3
        mutation_probability = 0.25
        mult = 3
        first_parent = self.clone_player(_first_parent)
        second_parent = self.clone_player(_second_parent)
        for i in range(len(first_parent.nn.weights)):
            for j in range(len(first_parent.nn.weights[i])):
                for k in range(len(first_parent.nn.weights[i][j])):
                    if random.uniform(0, 1) < mutation_probability:
                        first_parent.nn.weights[i][j][k] += np.random.normal(0, 1) * mult
                    if random.uniform(0, 1) < mutation_probability:
                        second_parent.nn.weights[i][j][k] += np.random.normal(0, 1) * mult
            for j in range(len(first_parent.nn.biases[i])):
                if random.uniform(0, 1) < mutation_probability:
                    first_parent.nn.biases[i][j] += np.random.normal(0, 1) * mult
                if random.uniform(0, 1) < mutation_probability:
                    second_parent.nn.biases[i][j] += np.random.normal(0, 1) * mult

        child_1 = Player(self.game_mode)
        child_2 = Player(self.game_mode)
        # make child weights as crossover
        for i in range(len(child_1.nn.weights)):
            child_1.nn.weights[i] = alpha * first_parent.nn.weights[i] + (1 - alpha) * second_parent.nn.weights[i]
            child_2.nn.weights[i] = alpha * second_parent.nn.weights[i] + (1 - alpha) * first_parent.nn.weights[i]

            child_1.nn.biases[i] = alpha * first_parent.nn.biases[i] + (1 - alpha) * second_parent.nn.biases[i]
            child_2.nn.biases[i] = alpha * second_parent.nn.biases[i] + (1 - alpha) * first_parent.nn.biases[i]
        # mutate in layers
        return child_1, child_2

    def clone_player(self, player):
        """
        Gets a player as an input and produces a clone of that player.
        """
        new_player = Player(self.game_mode)
        new_player.nn = copy.deepcopy(player.nn)
        new_player.fitness = player.fitness
        return new_player
