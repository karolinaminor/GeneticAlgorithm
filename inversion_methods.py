import random


class InversionMethods:
    """Class implementing inversion operations for chromosomes."""

    @staticmethod
    def two_point_inversion(genes):
        """
        Standard two-point inversion — reverse order of bits between two random points.
        """
        new_genes = []
        for gene in genes:
            if len(gene) < 3:
                new_genes.append(gene)
                continue
            i, j = sorted(random.sample(range(len(gene)), 2))
            mutated = gene[:i] + gene[i:j + 1][::-1] + gene[j + 1:]
            new_genes.append(mutated)
        return new_genes
