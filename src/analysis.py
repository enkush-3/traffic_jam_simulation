import numpy as np
from simulation import run_monte_carlo
from model import simulate_intersection

def calc_mean_wait(wait_times):
    if not wait_times:
        return 0.0
    return float(np.mean(wait_times))



def calc_confidence_interval(data):
    
    n = len(data)
    mean_val = np.mean(data)
    std_val = np.std(data, ddof=1)
    margin = 1.96 * std_val / np.sqrt(n)
    return mean_val, mean_val - margin, mean_val + margin




def find_optimal_signal(lam, duration_sec=3600, trials=100):

    configs = [(30, 60), (40, 50), (50, 40), (60, 30)]
    best_config = None
    min_wait = float('inf')
    results = {}
    
    for green, red in configs:
        _, waits = run_monte_carlo(lam, green, red, duration_sec, trials)
        mean_wait = np.mean(waits)
        results[f"{green}/{red}"] = mean_wait
        if mean_wait < min_wait:
            min_wait = mean_wait
            best_config = (green, red)
            
    return best_config, results