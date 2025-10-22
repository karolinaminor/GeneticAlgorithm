from genetic_algorithm import GeneticAlgorithm

if __name__ == "__main__":
    # test
    config = {
        'population_size': 4,
        'n_variables': 2,
        'bounds': [(0, 10), (0, 5)],
        'precision': 3,
        'p_mutation': 0.1,
        'p_inversion': 0.2
    }

    ga = GeneticAlgorithm(config)

    population = ga.initialize_population()
    print("Populacja początkowa:")
    for i, chrom in enumerate(population):
        print(f"  Chromosom {i+1}: {chrom.genes}")

    ga.run(epochs=3)
