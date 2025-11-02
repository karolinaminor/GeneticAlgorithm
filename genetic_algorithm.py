import random
import numpy as np
from chromosome import Chromosome
from crossover_methods import CrossoverMethods
from mutation_methods import MutationMethods
from inversion_methods import InversionMethods


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

    def run(self, epochs: int) -> tuple:
        """Run the genetic algorithm - test """

        self.initialize_population()

        for chrom in self.population:
            chrom.evaluate_fitness(self.fitness_function)

        history = []

        print("=== START GENETIC ALGORITHM ===")

        for epoch in range(epochs):
            print(f"\nEpoch {epoch + 1}/{epochs}")

            new_population = []

            elite = self._get_elite(self.population)
            new_population.extend(elite)

            while len(new_population) < len(self.population):
                parent1 = random.choice(self.population)
                parent2 = random.choice(self.population)
                while parent1 == parent2:
                    parent2 = random.choice(self.population)

                child1, child2 = self._crossover(parent1, parent2)

                child1 = self._mutation(child1)
                child1 = self._inversion(child1)
                child1.evaluate_fitness(self.fitness_function)

                if len(new_population) < len(self.population):
                    new_population.append(child1)

                if len(new_population) < len(self.population):
                    child2 = self._mutation(child2)
                    child2 = self._inversion(child2)
                    child2.evaluate_fitness(self.fitness_function)
                    new_population.append(child2)

            self.population = new_population

            print("Populacja po krzyżowaniu, mutacji i inwersji:")
            for i, c in enumerate(self.population):
                print(f"  Chromosom {i + 1}: {c.genes}, Fitness: {c.fitness}")
                print(f"Values: {c.decode()}")
            
            best_solution = self._get_best_solution()
            avg_fitness, max_fitness, min_fitness, std_fitness = self._calculate_stats()
            history.append({
                'epoch': epoch + 1,
                'best_solution': best_solution,
                'average_fitness': avg_fitness,
                'max_fitness': max_fitness,
                'min_fitness': min_fitness,
                'std_fitness': std_fitness
            })

            print(f"\nNajlepsze rozwiązanie w epoce {epoch + 1}:")
            print(f"  Chromosom: {best_solution.genes}, Fitness: {best_solution.fitness}")
            print(f"  Values: {best_solution.decode()}")

        print("\n=== NAJLEPSZE ROZWIĄZANIE PO WSZYSTKICH EPOKACH ===")
        print(f"  Chromosom: {best_solution.genes}, Fitness: {best_solution.fitness}")
        print(f"  Values: {best_solution.decode()}")

        print("\n=== KONIEC DZIAŁANIA ALGORYTMU ===")
        return best_solution, history

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
            gene = ''.join(['1' if random.random()
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

    def _crossover(self, parent1: Chromosome, parent2: Chromosome):
        """Perform crossover between two parent chromosomes."""
        method = self.config.get('crossover_method', 'one_point')

        offspring1_genes = []
        offspring2_genes = []

        for g1, g2 in zip(parent1.genes, parent2.genes):
            if method == 'one_point':
                o1, o2 = CrossoverMethods.one_point_crossover(g1, g2)
            elif method == 'two_point':
                o1, o2 = CrossoverMethods.two_point_crossover(g1, g2)
            elif method == 'uniform':
                o1, o2 = CrossoverMethods.uniform_crossover(g1, g2)
            elif method == 'discrete':
                o1 = CrossoverMethods.discrete_crossover(g1, g2)
                o2 = CrossoverMethods.discrete_crossover(g2, g1)
            else:
                raise ValueError(f"Unknown crossover method: {method}")

            offspring1_genes.append(o1)
            offspring2_genes.append(o2)

        return (
            Chromosome(offspring1_genes, parent1.bounds, parent1.precision),
            Chromosome(offspring2_genes, parent1.bounds, parent1.precision)
        )

    def _mutation(self, chromosome: Chromosome) -> Chromosome:
        """Use selected mutation method to on chromosome."""
        method = self.config.get('mutation_method', 'one_point')
        p_mutation = self.config.get('p_mutation', 0.05)

        if method == 'one_point':
            new_genes = MutationMethods.one_point_mutation(chromosome.genes, p_mutation)
        elif method == 'two_point':
            new_genes = MutationMethods.two_point_mutation(chromosome.genes)
        elif method == 'boundary':
            new_genes = MutationMethods.boundary_mutation(chromosome.genes)
        else:
            raise ValueError(f"Unknown mutation method: {method}")

        return Chromosome(new_genes, chromosome.bounds, chromosome.precision)

    def _inversion(self, chromosome: Chromosome) -> Chromosome:
        """Apply selected inversion method to a chromosome."""
        method = self.config.get('inversion_method', 'two_point')
        p_inversion = self.config.get('p_inversion', 0.05)

        if random.random() >= p_inversion:
            return chromosome

        if method == 'two_point':
            new_genes = InversionMethods.two_point_inversion(chromosome.genes)
        else:
            raise ValueError(f"Unknown inversion method: {method}")

        return Chromosome(new_genes, chromosome.bounds, chromosome.precision)

    def _get_elite(self, population: list) -> list:
        """
        Returns:
            list: Elite individuals to be carried over to the next generation
        """
        elite_p = self.config['elite_p']
        n_elite = max(1, int(len(population) * elite_p))

        reverse = True if self.config.get('optimization', 'max') == 'max' else False
        sorted_population = sorted(population, key=lambda c: c.fitness, reverse=reverse)

        return sorted_population[:n_elite]
    
    def _get_best_solution(self) -> Chromosome:
        """Return the best solution in the current population."""
        if not self.population:
            raise ValueError("Population is not initialized.")

        reverse = True if self.config.get('optimization', 'max') == 'max' else False
        best_chromosome = max(self.population, key=lambda c: c.fitness) if reverse else min(self.population, key=lambda c: c.fitness)

        return best_chromosome
    
    def _calculate_stats(self) -> dict:
        """Calculate statistics of the current population."""
        fitness_values = [chrom.fitness for chrom in self.population]
        avg_fitness = sum(fitness_values) / len(fitness_values)
        max_fitness = max(fitness_values)
        min_fitness = min(fitness_values)
        std_fitness = np.std(fitness_values)

        return {
            'average_fitness': avg_fitness,
            'max_fitness': max_fitness,
            'min_fitness': min_fitness,
            'std_fitness': std_fitness
        }
