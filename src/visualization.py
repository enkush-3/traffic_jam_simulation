import matplotlib.pyplot as plt
import numpy as np
from simulation import simulate_full_day, run_monte_carlo
from model import simulate_intersection

def plot_queue(queue_log: np.ndarray):
    plt.figure(figsize=(10, 5))
    plt.plot(queue_log, color='blue', alpha=0.7)
    plt.title("Дарааллын уртын өөрчлөлт (1 цаг)")
    plt.xlabel("Хугацаа (секунд)")
    plt.ylabel("Машины тоо")
    plt.grid(True)
    plt.savefig("queue_log.png")

def plot_hourly_queues():
    hourly_queues = simulate_full_day()
    hours = np.arange(24)
    
    plt.figure(figsize=(10, 5))
    plt.bar(hours, hourly_queues, color='orange', edgecolor='black')
    plt.title("24 цагийн цаг тутмын дундаж дарааллын урт")
    plt.xlabel("Цаг (0-23)")
    plt.ylabel("Дундаж дараалал")
    plt.xticks(hours)
    plt.grid(axis='y')
    plt.savefig("hourly_queues.png")

def plot_histogram(wait_times: list):
    plt.figure(figsize=(10, 5))
    plt.hist(wait_times, bins=30, color='purple', edgecolor='black', alpha=0.7)
    plt.title("Хүлээх хугацааны тархалтын хистограмм")
    plt.xlabel("Хүлээсэн хугацаа (машин)")
    plt.ylabel("Давтамж")
    plt.grid(True)
    plt.savefig("wait_times_histogram.png")
    

def plot_convergence():
    trials_list = [100, 500, 1000, 5000, 10000]
    means = []
    
    for n in trials_list:
        _, waits = run_monte_carlo(lam=15, green_sec=40, red_sec=50, duration_sec=3600, n_trials=n)
        means.append(np.mean(waits))
        
    plt.figure(figsize=(8, 5))
    plt.plot(trials_list, means, marker='o', linestyle='-', color='red', label="Дундаж утга")
    plt.xscale('log')
    plt.title("Давталтын тооноос хамаарсан тогтворжилт")
    plt.xlabel("Монте-Карло давталтын тоо (log scale)")
    plt.ylabel("Дундаж хүлээлт")
    plt.legend()
    plt.grid(True)
    plt.savefig("convergence_plot.png")


if __name__ == "__main__":
    plot_queue(simulate_intersection(lam=15, green_sec=40, red_sec=50, duration_sec=3600)[0])
    plot_hourly_queues()
    plot_histogram(simulate_intersection(lam=15, green_sec=40, red_sec=50, duration_sec=3600)[1])
    plot_convergence()

    plt.show()