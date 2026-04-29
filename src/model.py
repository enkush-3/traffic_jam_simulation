import numpy as np

def generate_arrivals(lam, duration_sec, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    lam_per_sec = lam / 60.0
    arrivals = rng.poisson(lam_per_sec, size=duration_sec)
    return arrivals

def simulate_intersection(lam=15, green_sec=40, red_sec=50, duration_sec=3600, rng=None):
    
    arrivals = generate_arrivals(lam, duration_sec, rng)
    cycle = green_sec + red_sec
    queue = 0
    queue_log = np.zeros(duration_sec)
    wait_times = []
    
    for t in range(duration_sec):
        queue += arrivals[t]
        phase = t % cycle
        if phase < green_sec and queue > 0:
            wait_times.append(queue)
            queue -= 1
        queue_log[t] = queue
        
    return queue_log, wait_times
