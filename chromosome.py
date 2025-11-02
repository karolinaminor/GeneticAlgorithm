
class Chromosome:
    """Binary representation of a chromosome"""

    def __init__(self, genes, bounds, precision):
        if not isinstance(genes, list) or not all(isinstance(g, str) for g in genes):
            raise ValueError("Genes must be a list of binary strings.")
        if not isinstance(bounds, list) or not all(isinstance(b, tuple) and len(b) == 2 for b in bounds):
            raise ValueError(
                "Bounds must be a list of tuples with two numeric values.")
        if not isinstance(precision, int) or precision < 0:
            raise ValueError("Precision must be a non-negative integer.")
        if len(genes) != len(bounds):
            raise ValueError(
                "The number of genes must match the number of bounds.")

        self.genes = genes
        self.bounds = bounds
        self.precision = precision
        self.fitness = None

    def decode(self):
        """Decode binary chromosome to real values"""
        decoded_values = []
        for i, gene in enumerate(self.genes):
            bound = self.bounds[i]
            m = len(gene)
            int_value = int(gene, 2)
            real_value = bound[0] + int_value * \
                (bound[1] - bound[0]) / (2**m - 1)
            real_value = round(real_value, self.precision)
            decoded_values.append(real_value)
        return decoded_values

    def evaluate_fitness(self, func=None):
        """Evaluate the fitness of the chromosome using the provided function."""
        if func is None:
            raise ValueError(
                "A fitness function must be provided to evaluate the chromosome.")

        decoded = self.decode()
        self.fitness = func(decoded)
        return self.fitness
