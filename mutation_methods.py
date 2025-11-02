import random


class MutationMethods:

    @staticmethod
    def one_point_mutation(genes, p_mutation):
        """
        Classic bit-flip mutation: for each bit, flip with probability p_mutation.
        """
        new_genes = []
        for gene in genes:
            mutated = ''.join(
                '1' if bit == '0' and random.random() < p_mutation else
                '0' if bit == '1' and random.random() < p_mutation else bit
                for bit in gene
            )
            new_genes.append(mutated)
        return new_genes

    @staticmethod
    def two_point_mutation(genes):
        """
        Two-point mutation: choose two random points and reverse the bits between them.
        (mutation applied to each gene independently)
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

    @staticmethod
    def boundary_mutation(genes):
        """
        Boundary mutation: flip only the first and last bits of the gene.
        """
        new_genes = []
        for gene in genes:
            if len(gene) < 2:
                new_genes.append(gene)
                continue
            mutated = (
                ('1' if gene[0] == '0' else '0') +
                gene[1:-1] +
                ('1' if gene[-1] == '0' else '0')
            )
            new_genes.append(mutated)
        return new_genes
