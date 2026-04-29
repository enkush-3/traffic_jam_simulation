import numpy as np
from model import simulate_intersection


def run_monte_carlo(lam, green_sec, red_sec, duration_sec, n_trials):

    rng = np.random.default_rng()
    all_mean_queues = []
    all_mean_waits = []
    
    for _ in range(n_trials):
        queue_log, wait_times = simulate_intersection(lam, green_sec, red_sec, duration_sec, rng=rng)
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
    


def simulate_full_day(green_sec: int = 40, red_sec: int = 50):

    rng = np.random.default_rng()
    hourly_queues = []
    
    for hour in range(24):
        lam = get_lambda_for_hour(hour)

        queue_log, _ = simulate_intersection(lam, green_sec, red_sec, 3600, rng=rng)
        hourly_queues.append(np.mean(queue_log))
        
    return hourly_queues




def simulate_4_directions(lam_ew: float = 15.0, lam_ns: float = 15.0, duration_sec: int = 3600):

    rng = np.random.default_rng()
    q_zb, w_zb = simulate_intersection(lam_ew, 40, 50, duration_sec, rng=rng)
    q_bz, w_bz = simulate_intersection(lam_ew, 40, 50, duration_sec, rng=rng)
    

    q_ho, w_ho = simulate_intersection(lam_ns, 50, 40, duration_sec, rng=rng)
    q_oh, w_oh = simulate_intersection(lam_ns, 50, 40, duration_sec, rng=rng)
    
    all_waits = w_zb + w_bz + w_ho + w_oh
    return np.mean(all_waits) if all_waits else 0

