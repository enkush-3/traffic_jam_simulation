import numpy as np
from simulation import run_monte_carlo
from model import simulate_intersection


def calc_confidence_interval(data):
    n = len(data)
    mean_val = np.mean(data)
    std_val = np.std(data, ddof=1)
    margin = 1.96 * std_val / np.sqrt(n)
    return mean_val, mean_val - margin, mean_val + margin

def find_optimal_signal(lam, configs, duration_sec=3600):
    results = {}
    best_wait = float('inf')
    best_config = None
    
    rng = np.random.default_rng()
    
    for green, red in configs:
        queue_log, wait_times = simulate_intersection(lam, green, red, duration_sec, rng=rng)
        avg_queue = np.mean(queue_log)
        avg_wait = np.mean(wait_times) if len(wait_times) > 0 else 0.0
        results[(green, red)] = (avg_queue, avg_wait)
        
        if avg_wait < best_wait:
            best_wait = avg_wait
            best_config = (green, red)
    
    return best_config, best_wait, results