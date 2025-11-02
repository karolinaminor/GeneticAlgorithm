import random


class SelectionMethods:
    """Class for implementing various selection methods in genetic algorithm."""

    @staticmethod
    def best_selection(population: list, num_select: int, minimize: bool) -> list:
        """Select the best individuals based on fitness."""
        sorted_pop = sorted(
            population, key=lambda x: x.fitness, reverse=not minimize)
        return sorted_pop[:num_select]

    # in this implementation, individuals can be selected multiple times - decide if this is desired
    # other possible way is to draw without replacement, but then difficulut to to resolve both parameters: num_select and tournament_size
    @staticmethod
    def tournament_selection(population: list, tournament_size: int, num_select: int, minimize: bool) -> list:
        """Select individuals using tournament selection."""
        selected = []
        for _ in range(num_select):
            tournament = random.sample(population, tournament_size)
            winner = min(tournament, key=lambda x: x.fitness) if minimize else max(
                tournament, key=lambda x: x.fitness)
            selected.append(winner)
        return selected

    @staticmethod
    def roulette_wheel_selection(population: list, num_select: int, minimize: bool) -> list:
        """Select individuals using roulette wheel selection."""
        roulette_population = population.copy()
        if minimize:
            for ind in roulette_population:
                ind.fitness = 1 / (ind.fitness + 1e-10)
        total_fitness = sum(ind.fitness for ind in roulette_population)
        probabilities = [ind.fitness /
                         total_fitness for ind in roulette_population]
        selected = random.choices(
            roulette_population, weights=probabilities, k=num_select)
        return selected
