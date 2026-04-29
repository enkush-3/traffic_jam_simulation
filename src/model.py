import numpy as np

def generate_arrivals(lam, duration_sec, rng=None):

    if rng is None:
        rng = np.random.default_rng()
    lam_per_sec = lam / 60.0
    arrivals = rng.poisson(lam_per_sec, size=duration_sec)
    return arrivals



def simulate_intersection(lam, green_sec, red_sec, duration_sec, rng=None):
    
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




# def generate_arrivals(lam, duration_sec, rng=None):
#     """
#     Пуассоны тархалтаар машины ирэлтийг үүсгэнэ.
#     Parameters:
#     lam : float -- минутад ирэх машины дундаж тоо
#     duration_sec : int -- хугацаа (секундээр)
#     rng : np.random.Generator -- seed удирдах
#     Returns:
#     arrivals : np.ndarray -- секунд бүрд ирсэн машины тоо
#     """
#     if rng is None:
#         rng = np.random.default_rng()
#     lam_per_sec = lam / 60.0
#     arrivals = rng.poisson(lam_per_sec, size=duration_sec)
#     return arrivals


# def simulate_intersection(lam, green_sec, red_sec, duration_sec, rng=None):
#     """
#     Нэг чиглэлийн уулзварын симуляц.
#     9Returns:
#     queue_log : np.ndarray -- секунд бүрийн дарааллын урт
#     wait_times : list -- машин бүрийн хүлээсэн хугацаа
#     """
#     arrivals = generate_arrivals(lam, duration_sec, rng)
#     cycle = green_sec + red_sec
#     queue = 0
#     queue_log = np.zeros(duration_sec)
#     wait_times = []
#     for t in range(duration_sec):
#         queue += arrivals[t]
#         phase = t % cycle
#         if phase < green_sec and queue > 0:
#             wait_times.append(queue)
#             queue -= 1
#         queue_log[t] = queue
#     return queue_log, wait_times
