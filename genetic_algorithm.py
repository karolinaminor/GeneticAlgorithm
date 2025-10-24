import numpy as np
from chromosome import Chromosome
import functions


class GeneticAlgorithm:
    """Main Genetic Algorithm implementation"""

    def __init__(self, config: dict, fitness_function):
        self._validate_config(config)
        if fitness_function is None:
            raise ValueError("A fitness function must be provided for the Genetic Algorithm.")
        self.config = config
        self.fitness_function = fitness_function
        self.population = None



    def initialize_population(self) -> list:
        """Initialize population with random binary chromosomes"""
        population_size = self.config['population_size']
        n_variables = self.config['n_variables']
        bounds = self.config['bounds']
        precision = self.config['precision']

        population = []

        for _ in range(population_size):
            chromosome = self._generate_chromosome(
                n_variables, bounds, precision)
            population.append(chromosome)

        self.population = population
        return population

    def run(self, epochs: int):
        """Run the genetic algorithm - test """

        self.initialize_population()

        for chrom in self.population:
            chrom.evaluate_fitness(self.fitness_function)

        print("=== START GENETIC ALGORITHM ===")

        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")

            new_population = []

            elite = self.get_elite(self.population)
            new_population.extend(elite)

            while len(new_population) < len(self.population):

                parent = __import__('random').choice(self.population)
                child = self.mutation(parent)
                child = self.inversion(child, self.config['p_inversion'])
                child.evaluate_fitness(self.fitness_function)

                new_population.append(child)

            self.population = new_population

            print("Populacja after elitism strategy, mutatnion and inversion:")
            for i, c in enumerate(self.population):
                print(f"  Chromosom {i + 1}: {c.genes}, Fitness: {c.fitness}")
                print(f"Values: {c.decode()}")

        print("\n=== KONIEC DZIAŁANIA ALGORYTMU ===")

    def _calculate_gene_length(self, bound, precision):
        """Calculate the length of the gene for a given variable based on bounds and precision"""
        len_range = bound[1] - bound[0]
        m = np.ceil(np.log2(len_range * (10 ** precision)))
        return int(m)

    def _generate_chromosome(self, n_variables, bounds, precision):
        """Generate a random binary chromosome"""
        genes = []
        for i in range(n_variables):
            bound = bounds[i]
            m = self._calculate_gene_length(bound, precision)
            gene = ''.join(['1' if __import__('random').random()
                                   > 0.5 else '0' for _ in range(m)])
            genes.append(gene)
        return Chromosome(genes, bounds, precision)

    def _validate_config(self, config: dict):
        """Validate configuration parameters"""

        required_keys = ['population_size', 'n_variables', 'bounds', 'precision', 'p_mutation', 'p_inversion', 'elite_p']

        for key in required_keys:
            if key not in config:
                raise ValueError(f"Missing required config parameter: {key}")

        if not isinstance(config['population_size'], int) or config['population_size'] <= 0:
            raise ValueError("population_size must be a positive integer")

        if not isinstance(config['n_variables'], int) or config['n_variables'] <= 0:
            raise ValueError("n_variables must be a positive integer")

        if not isinstance(config['bounds'], list) or len(config['bounds']) != config['n_variables']:
            raise ValueError(
                "bounds must be a list with length equal to n_variables")

        for bound in config['bounds']:
            if (not isinstance(bound, tuple) or len(bound) != 2 or
                    not all(isinstance(x, (int, float)) for x in bound) or
                    bound[0] >= bound[1]):
                raise ValueError(
                    "Each bound must be a tuple of two numbers (min, max) with min < max")

        if not isinstance(config['precision'], int) or config['precision'] <= 0:
            raise ValueError("precision must be a positive integer")

        if not isinstance(config['p_mutation'], (int, float)) or not (0 <= config['p_mutation'] <= 1):
            raise ValueError("'p_mutation' must be between 0 and 1")

        if not isinstance(config['p_inversion'], (int, float)) or not (0 <= config['p_inversion'] <= 1):
            raise ValueError("'p_inversion' must be between 0 and 1")

        if not isinstance(config['elite_p'], (int, float)) or not (0 <= config['elite_p'] <= 1):
            raise ValueError("'elite_p' must be between 0 and 1")

        if 'optimization' not in config:
            raise ValueError("Missing required config parameter: 'optimization'")

        if config['optimization'] not in ('min', 'max'):
            raise ValueError("'optimization' must be either 'min' or 'max'")



    def mutation(self, chromosome: Chromosome) -> Chromosome:
            """ chromosome mutation """

            p_mutation = self.config['p_mutation']

            new_genes = []
            for gene in chromosome.genes:
                new_gene = ''
                for bit in gene:
                    if __import__('random').random() < p_mutation:
                        new_gene += '0' if bit == '1' else '1'
                    else:
                        new_gene += bit
                new_genes.append(new_gene)

            return Chromosome(new_genes, chromosome.bounds, chromosome.precision)

    def inversion(self, chromosome: Chromosome, p_inversion: float) -> Chromosome:
            """ chromosome inversion """

            if __import__('random').random() < p_inversion:
                full_gene = ''.join(chromosome.genes)
                i, j = sorted(__import__('random').sample(range(len(full_gene)), 2))
                inverted = full_gene[:i] + full_gene[i:j + 1][::-1] + full_gene[j + 1:]

                new_genes = []
                index = 0

                for g in chromosome.genes:
                    length = len(g)
                    new_genes.append(inverted[index:index + length])
                    index += length

                return Chromosome(new_genes, chromosome.bounds, chromosome.precision)
            return chromosome

    def get_elite(self, population: list) -> list:
        """
        Returns:
            list: Elite individuals to be carried over to the next generation
        """
        elite_p = self.config['elite_p']
        n_elite = max(1, int(len(population) * elite_p))

        reverse = True if self.config.get('optimization', 'max') == 'max' else False
        sorted_population = sorted(population, key=lambda c: c.fitness, reverse=reverse)

        return sorted_population[:n_elite]
