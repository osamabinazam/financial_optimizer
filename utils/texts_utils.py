def get_text_for_algorithms_combo_box():
    return [
        "Particle Swarm Optimization (PS0)",
        "Differential Evolution (DE)",
        "Simulated Annealing (SA)",
        "Genetic Algorithm (GA)",
        "Covariance Matrix Adaptation Evolution Strategy (CMA-ES)",
        "Tabu Search",
        "TokenRing Search"
    ]


def get_text_for_risk_metrics_combo_box():
    return [
        "Omega",
        "Sharp-Squared",
        "Sortino",
        "Rachev",
        "Information",
        "Calmar",
        "CVaR",
    ]


def get_text_for_time_frames_combo_box():
    return [
        "Daily",
        "Weekly",
        "Bi-Weekly"
        "Monthly",
        "Quarterly",
        "Semi-Annually",
    ]

def description():
    return "Analyze and optimize your financial portfolios with advanced risk metrics and algorithms."
