"""Example Implementation of SIMPLE ES algorithm"""

import sys
import os

DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # noqa
sys.path.insert(0, DIR)  # noqa

from gerel.genome.factories import minimal
from gerel.algorithms.SIMPLE.population import SIMPLEPopulation
from gerel.algorithms.SIMPLE.mutator import SIMPLEMutator
from gerel.populations.genome_seeders import curry_genome_seeder
import numpy as np
from examples.utils import build_simple_env


def simple_simple_example():
    genome = minimal(
        input_size=1,
        output_size=1
    )

    weights_len = len(genome.edges) + len(genome.nodes)
    init_mu = np.random.uniform(-3, 3, weights_len)

    mutator = SIMPLEMutator(
        std_dev=0.01,
        survival_rate=0.01
    )

    seeder = curry_genome_seeder(
        mutator=mutator,
        seed_genomes=[genome]
    )

    population = SIMPLEPopulation(
        population_size=1000,
        genome_seeder=seeder
    )

    target_mu = np.random.uniform(-3, 3, len(init_mu))
    assign_population_fitness = build_simple_env(target_mu)

    for i in range(100):
        assign_population_fitness(population)
        mutator(population)
        weights = np.array([genome.weights for genome in population.genomes])
        mu = weights.mean(axis=0)
        loss = np.linalg.norm(mu - target_mu)
        print(f'generation: {i}, loss: {loss}')


if __name__ == '__main__':
    simple_simple_example()
