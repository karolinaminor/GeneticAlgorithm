import random


class CrossoverMethods:
    """Class for implementing various crossover methods in genetic algorithm."""

    # methods are working on one gene
    # in genetic_algoritm need to iterate over all genes and check if crossover occurs
    @staticmethod
    def one_point_crossover(gene1, gene2):
        """Perform one-point crossover for one gene between two parents."""
        if len(gene1) != len(gene2):
            raise ValueError("Genes must be of the same length for crossover.")
        point = random.randint(1, len(gene1) - 1)
        offspring1 = gene1[:point] + gene2[point:]
        offspring2 = gene2[:point] + gene1[point:]
        return offspring1, offspring2

    @staticmethod
    def two_point_crossover(gene1, gene2):
        """Perform two-point crossover for one gene between two parents."""
        if len(gene1) != len(gene2):
            raise ValueError("Genes must be of the same length for crossover.")
        point1 = random.randint(1, len(gene1) - 2)
        point2 = random.randint(point1 + 1, len(gene1) - 1)
        offspring1 = gene1[:point1] + gene2[point1:point2] + gene1[point2:]
        offspring2 = gene2[:point1] + gene1[point1:point2] + gene2[point2:]
        return offspring1, offspring2

    @staticmethod
    def uniform_crossover(gene1, gene2, p=0.5):
        """Perform uniform crossover for one gene between two parents."""
        if len(gene1) != len(gene2):
            raise ValueError("Genes must be of the same length for crossover.")
        offspring1 = []
        offspring2 = []
        for b1, b2 in zip(gene1, gene2):
            if random.random() < p:
                offspring1.append(b2)
                offspring2.append(b1)
            else:
                offspring1.append(b1)
                offspring2.append(b2)
        return ''.join(offspring1), ''.join(offspring2)

    @staticmethod
    def discrete_crossover(gene1, gene2):
        """Perform discrete crossover for one gene between two parents."""
        if len(gene1) != len(gene2):
            raise ValueError("Genes must be of the same length for crossover.")
        offspring1 = []
        for b1, b2 in zip(gene1, gene2):
            if random.random() < 0.5:
                offspring1.append(b1)
            else:
                offspring1.append(b2)
        return ''.join(offspring1)