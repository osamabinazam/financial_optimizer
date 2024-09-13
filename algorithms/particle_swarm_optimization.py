import numpy as np
import pandas as pd
import pygmo as pg

from utils.performance_matrics import calculate_portfolio_metrics, calculate_benchmark_stock_metrics
from utils.risk_matrics import calculate_returns, risk_averse_method


class PortfolioOptimizer:
    def __init__(self, returns, metric="sharp", penalty_factor=1000, risk_free_rate=0.02 / 252):
        """
        Initialize the PortfolioOptimizer class with the provided parameters. The default metric is the Sharpe ratio.
        :param returns:
        :param metric:
        :param penalty_factor:
        :param risk_free_rate:
        """

        self.returns = returns
        self.metric = metric
        self.penalty_factor = penalty_factor
        self.risk_free_rate = 0.02 / 252

    def fitness(self, weights):
        """
       The fitness function for PSO optimization. It computes the risk-adjusted return based on the selected metric.
        :param weights: Portfolio weights to evaluate.
        :return: The negative of the performance metric to minimize.
        """
        portfolio_return = np.dot(self.returns.mean(), weights)
        portfolio_votality = np.sqrt(np.dot(weights.T, np.dot(self.returns.cov(), weights)))

        # Use the risk_avers_method to calculate the selected metric (e.g, Sharpe Ratio)
        portfolio_metric = risk_averse_method(portfolio_return, portfolio_votality, self.metric, self.returns,
                                              self.risk_free_rate)

        # penalty if the weight don't sum to 1
        penalty = self.penalty_factor * (np.sum(weights) - 1) ** 2

        return [-portfolio_metric + penalty]

    def get_bounds(self):
        """
        Defines the lower and upper bounds for portfolio weights (0 to 1 for each asset).
        :return: Tuple of bounds
        """
        return ([0.0] * len(self.returns.columns), [1.0] * len(self.returns.columns))


def run_pso_optimization(returns, metric='sharp_ratio', risk_free_rate=0.02 / 252):
    """
    Runs the PSO algorithm to optimize the portfolio based on the selected metric.
    :param returns: DataFrame of portfolio returns.
    :param metric: The performance metric to optimize (e.g., Sharpe Ratio, Sortino Ratio, etc.).
    :param risk_free_rate: The risk-free rate for calculating metrics.
    :return: The best portfolio weights and performance metric.
    """

    # Initialize the portfolio optimization problem.
    udp = PortfolioOptimizer(returns, metric=metric, risk_free_rate=risk_free_rate)

    # Create the optimization problem
    prob = pg.problem(udp)

    # Create the PSO algorithm
    algo = pg.algorithm(pg.pso(gen=1000))

    # Initialize a population and evolve
    pop = pg.population(prob, size=50)
    pop = algo.evolve(pop)

    # Get the best weights and  best (negative) metric value (minimized, so we negate it)
    best_weights = pop.champion_x
    best_metric_value = -pop.champion_x[0]  # negate since pygmo minimizes

    return best_weights, best_metric_value
