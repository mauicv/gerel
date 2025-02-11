"""Example Implementation of NEAT algorithm from
see http://nn.cs.utexas.edu/downloads/papers/stanley.ec02.pdf

Note: The we use restricted networks in the sense all edges point forwards.
"""


import sys
import os

DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))  # noqa
sys.path.insert(0, DIR)  # noqa

from gerel.algorithms.NEAT.population import NEATPopulation
from gerel.algorithms.NEAT.mutator import NEATMutator
from gerel.algorithms.NEAT.metric import generate_neat_metric
from gerel.populations.genome_seeders import curry_genome_seeder
from gerel.util.datastore import DataStore
from gerel.genome.factories import minimal
from examples.utils import build_env, make_counter_fn


def neat_bipedal_walker():
    pop_size = 400
    mutator = NEATMutator(
        new_edge_probability=0.1,
        new_node_probability=0.05
    )
    genome = minimal(
        input_size=24,
        output_size=4,
        depth=5
    )
    seeder = curry_genome_seeder(
        mutator=mutator,
        seed_genomes=[genome]
    )
    metric = generate_neat_metric(
        c_1=1,
        c_2=1,
        c_3=3
    )
    population = NEATPopulation(
        population_size=pop_size,
        delta=4,
        genome_seeder=seeder,
        metric=metric
    )

    ds = DataStore(name='bip_walker_NEAT_data')

    assign_population_fitness = build_env(
        env_name='BipedalWalker-v3',
        num_steps=200,
        repetition=1)
    counter_fn = make_counter_fn()

    for i in range(500):
        success = assign_population_fitness(population)
        if success and counter_fn():
            break
        population.speciate()
        data = population.to_dict()
        mutator(population)
        ds.save(data)
        print_progress(data)
    return True


def print_progress(data):
    data_string = ''
    for val in ['generation', 'best_fitness', 'worst_fitness', 'mean_fitness']:
        data_string += f' {val}: {data[val]}'
    print(data_string)


if __name__ == "__main__":
    neat_bipedal_walker()
