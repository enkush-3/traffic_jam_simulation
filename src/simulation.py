import numpy as np
from model import simulate_intersection


def run_monte_carlo(lam=15, green_sec=40, red_sec=50, duration_sec=3600, n_trials=1000):
    all_mean_queues = []
    all_mean_waits = []
    
    for _ in range(n_trials):
        queue_log, wait_times = simulate_intersection(lam, green_sec, red_sec, duration_sec)
        all_mean_queues.append(np.mean(queue_log))
        if len(wait_times) > 0:
            all_mean_waits.append(np.mean(wait_times))
        else:
            all_mean_waits.append(0)
            
    return np.array(all_mean_queues), np.array(all_mean_waits)


def get_lambda_for_hour(hour):
    if (8 <= hour <= 9) or (17 <= hour <= 19):
        return 25.0
    elif 9 < hour < 17:
        return 15.0
    elif (22 <= hour <= 23) or (0 <= hour <= 6):
        return 3.0
    else:
        return 10.0

def simulate_24h_one_direction(green_sec: int, red_sec: int, duration_per_hour: int = 3600):
    hourly_mean_queue = np.zeros(24)
    hourly_mean_wait = np.zeros(24)
    rng = np.random.default_rng()
    
    for hour in range(24):
        lam = get_lambda_for_hour(hour)
        queue_log, wait_times = simulate_intersection(lam, green_sec, red_sec, duration_per_hour, rng=rng)
        hourly_mean_queue[hour] = np.mean(queue_log)
        if len(wait_times) > 0:
            hourly_mean_wait[hour] = np.mean(wait_times)
        else:
            hourly_mean_wait[hour] = 0.0
    return hourly_mean_queue, hourly_mean_wait

def _compute_comparison_stats(real_lam, sim_lam, green, red, duration_sec=3600):
    """Хоёр λ-ийн симуляцийн статистикийг тооцоолж буцаана."""
    q_real, w_real = simulate_intersection(real_lam, green, red, duration_sec)
    q_sim, w_sim = simulate_intersection(sim_lam, green, red, duration_sec)
    stats = {
        "real": {
            "queue": np.mean(q_real),
            "wait": np.mean(w_real) if w_real else 0.0,
            "total": len(w_real)
        },
        "sim": {
            "queue": np.mean(q_sim),
            "wait": np.mean(w_sim) if w_sim else 0.0,
            "total": len(w_sim)
        },
        "q_real": q_real,
        "q_sim": q_sim,
        "w_real": w_real,
        "w_sim": w_sim
    }
    return stats


