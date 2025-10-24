from genetic_algorithm import GeneticAlgorithm
import benchmark_functions as bf

if __name__ == "__main__":
    # test
    config = {
        'population_size': 10,
        'n_variables': 2,
        'bounds': [(-3, 4), (-3, 4)],
        'precision': 3,
        'p_mutation': 0.09,
        'p_inversion': 0.09,
        'elite_p': 0.15,
        'optimization': 'min'
    }

    ga = GeneticAlgorithm(config, bf.McCormick())

    ga.run(epochs=125)
