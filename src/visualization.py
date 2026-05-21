import matplotlib.pyplot as plt
import numpy as np
from simulation import _compute_comparison_stats, simulate_24h_one_direction, run_monte_carlo
from model import simulate_intersection
from analysis import find_optimal_signal, calc_confidence_interval

import matplotlib.pyplot as plt
import numpy as np
import os
OUTPUT_DIR = "output/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_one_hour_direction_queue():
    queue_log, wait_times = run_monte_carlo(n_trials=100)
    
    total_vehicles = len(wait_times)
    avg_wait = np.mean(wait_times) if total_vehicles > 0 else 0.0
    avg_queue = np.mean(queue_log)
    time_axis = np.arange(len(queue_log))
    
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 1, 1)
    plt.plot(time_axis, queue_log, linewidth=1, color='blue', label=f'Дарааллын дундаж урт: {avg_queue:.2f}')
    plt.title('Нэг чиглэлийн дарааллын урт (секунд тутам)')
    plt.xlabel('Давталт')
    plt.ylabel('Дараалалд байгаа машины тоо')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(2, 1, 2)
    vehicle_index = np.arange(total_vehicles)
    plt.scatter(vehicle_index, wait_times, s=10, color='red', alpha=0.7, label=f'Хүлээх хугацаа: {avg_wait:.2f} сек')
    plt.title('Нэвтэрсэн машин бүрийн хүлээх хугацаа')
    plt.xlabel('Давталт бүрийн дундаж машины дугаар')
    plt.ylabel('Давталт')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()

    plt.savefig(f'{OUTPUT_DIR}A.one_direction_queue_wait.png')

def plot_4_directions_queue():
    
    ql_right, wt_right = run_monte_carlo(n_trials=100)
    ql_left, wt_left   = run_monte_carlo(n_trials=100)
    ql_up, wt_up       = run_monte_carlo(n_trials=100, green_sec=50, red_sec=40)
    ql_down, wt_down   = run_monte_carlo(n_trials=100, green_sec=50, red_sec=40)

    fig1, axes1 = plt.subplots(2, 2, figsize=(14, 10))
    directions = [('Баруун', ql_right), ('Зүүн', ql_left), ('Дээш', ql_up), ('Доош', ql_down)]
    
    for ax, (name, queue) in zip(axes1.flat, directions):
        time_axis = np.arange(len(queue))
        avg_q = np.mean(queue)
        ax.plot(time_axis, queue, linewidth=1, color='blue', label=f'Дундаж: {avg_q:.2f}')
        ax.set_title(f'{name} чиглэл - Дарааллын урт')
        ax.set_xlabel('Давталт')
        ax.set_ylabel('Машины тоо')
        ax.grid(True, alpha=0.3)
        ax.legend(loc='upper right')
    fig1.suptitle('4 чиглэлийн дарааллын уртын харьцуулалт', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}B-1.four_directions_queue.png')



    fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))
    wait_dirs = [('Баруун', wt_right), ('Зүүн', wt_left), ('Дээш', wt_up), ('Доош', wt_down)]
    
    for ax, (name, waits) in zip(axes2.flat, wait_dirs):
        total = len(waits)
        if total > 0:
            avg_w = np.mean(waits)
            ax.scatter(np.arange(total), waits, s=10, color='red', alpha=0.5,
                       label=f'Дундаж: {avg_w:.2f} сек')
            ax.legend(loc='upper right')
        else:
            ax.text(0.5, 0.5, 'Машин гарсангүй', transform=ax.transAxes, ha='center')
        ax.set_title(f'{name} чиглэл - Хүлээх хугацаа')
        ax.set_xlabel('Давталт')
        ax.set_ylabel('Хүлээх хугацаа [секунд]')
        ax.grid(True, alpha=0.3)
    fig2.suptitle('4 чиглэлийн хүлээх хугацааны харьцуулалт', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}B-2.four_directions_wait.png')
    

def plot_24h_four_directions():
    configs = [
        ('Зүүн', 40, 50),
        ('Баруун', 40, 50),
        ('Хойно', 50, 40),
        ('Өмнө', 50, 40)
    ]
    
    fig1, axes1 = plt.subplots(2, 2, figsize=(14, 10))
    fig2, axes2 = plt.subplots(2, 2, figsize=(14, 10))
    
    hours_axis = np.arange(24)
    
    for ax_q, ax_w, (name, green, red) in zip(axes1.flat, axes2.flat, configs):
        q_mean, w_mean = simulate_24h_one_direction(green, red)
        
        ax_q.plot(hours_axis, q_mean, marker='o', linestyle='-', color='blue')
        ax_q.set_title(f'{name} - Дарааллын дундаж')
        ax_q.set_xlabel('Цаг (0-23)')
        ax_q.set_ylabel('Дундаж машин')
        ax_q.grid(True, alpha=0.3)
        
        ax_w.plot(hours_axis, w_mean, marker='s', linestyle='-', color='red')
        ax_w.set_title(f'{name} - Хүлээх хугацааны дундаж')
        ax_w.set_xlabel('Цаг (0-23)')
        ax_w.set_ylabel('Секунд')
        ax_w.grid(True, alpha=0.3)
    
    fig1.suptitle('24 цагийн дарааллын урт (4 чиглэл)', fontsize=16)
    fig2.suptitle('24 цагийн хүлээх хугацаа (4 чиглэл)', fontsize=16)
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}C.24h_four_directions.png')
    

def plot_optimal_signal(lams=None, descriptions=None, configs=None):
    if lams is None:
        lams = [25, 10]
    if descriptions is None:
        descriptions = ["Оргил цаг", "Оргил бус цаг"]
    if configs is None:
        configs = [(30, 60), (40, 50), (50, 40), (60, 30)]
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    config_labels = [f"{g}/{r}" for g, r in configs]
    
    for idx, (lam, desc) in enumerate(zip(lams, descriptions)):

        best_cfg, best_w, results = find_optimal_signal(lam, configs)
        print_optimal_signal(lam, results, best_cfg, best_w) 
        
        ax1 = axes[idx]
        x = np.arange(len(config_labels))
        width = 0.35
        
        avg_queues = [v[0] for v in results.values()]
        avg_waits = [v[1] for v in results.values()]
        

        bars_q = ax1.bar(x - width/2, avg_queues, width, color='#4C72B0', alpha=0.8, label='Дундаж дараалал')
        ax1.set_xlabel('Ногоон/Улаан (с)')
        ax1.set_ylabel('Дундаж дараалал (машин)', color='#4C72B0')
        ax1.tick_params(axis='y', labelcolor='#4C72B0')
        ax1.set_xticks(x)
        ax1.set_xticklabels(config_labels)
        ax1.grid(axis='y', alpha=0.3)
        
        ax2 = ax1.twinx()
        bars_w = ax2.bar(x + width/2, avg_waits, width*0.8, color='#DD8452', alpha=0.8, label='Дундаж хүлээлт')
        ax2.set_ylabel('Дундаж хүлээлт (сек)', color='#DD8452')
        ax2.tick_params(axis='y', labelcolor='#DD8452')
        
        for bar in bars_q:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.02, f'{height:.2f}',
                     ha='center', va='bottom', fontsize=8, color='#4C72B0')
        for bar in bars_w:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.02, f'{height:.2f}',
                     ha='center', va='bottom', fontsize=8, color='#DD8452')
        
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=8)
        
        ax1.set_title(f'{desc} (λ = {lam})')
    
    fig.suptitle('Гэрлэн дохионы хуваарилалтын харьцуулалт', fontsize=14)
    fig.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}D.optimal_signal_comparison.png')

def plot_histogram_wait_times():
    _, wait_times = simulate_intersection()
    plt.figure(figsize=(12, 8))
    plt.hist(wait_times, bins=30, color='coral', edgecolor='black')
    plt.title('Хүлээх хугацааны тархалт')
    plt.xlabel('Хүлээх хугацаа (сек)')
    plt.ylabel('Машины тоо')
    plt.grid(axis='y', alpha=0.3)
    plt.savefig(f'{OUTPUT_DIR}E-1.wait_time_histogram.png')


def plot_convergence_and_confidence():
    lam = 15
    N_list = [100, 500, 1000, 5000, 10000]
    means = []
    lows = []
    highs = []
    
    for N in N_list:
        mean_queues, mean_waits = run_monte_carlo(lam=lam, green_sec=40, red_sec=50,
                                                 duration_sec=3600, n_trials=N)
        overall_mean, low, high = calc_confidence_interval(mean_waits)
        means.append(overall_mean)
        lows.append(low)
        highs.append(high)
    
    print_convergence_table(N_list, means, lows, highs, lam=lam)
    errors = [highs[i] - means[i] for i in range(len(N_list))]
    
    plt.figure(figsize=(8,5))
    plt.errorbar(N_list, means, yerr=errors, fmt='o-', capsize=5, color='navy')
    plt.xlabel('Давталтын тоо (N)')
    plt.ylabel('Дундаж хүлээх хугацаа (сек)')
    plt.title('Монте-Карло давталтын тогтворжилт')
    plt.grid(True, alpha=0.3)
    plt.savefig(f'{OUTPUT_DIR}E-2.monte_carlo_convergence.png')


def plot_comparison(real_lam=26.666, sim_lam=15, green=60, red=30, duration_sec=3600):
    """Бодит өгөгдөл ба загварын харьцуулалтын графикийг зурж хадгална."""
    stats = _compute_comparison_stats(real_lam, sim_lam, green, red, duration_sec)
    q_real = stats["q_real"]
    q_sim  = stats["q_sim"]
    w_real = stats["w_real"]
    w_sim  = stats["w_sim"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    time_axis = np.arange(duration_sec)
    ax1.plot(time_axis, q_real, linewidth=0.6, alpha=0.9, label=f"Бодит (λ={real_lam})")
    ax1.plot(time_axis, q_sim, linewidth=0.6, alpha=0.9, label=f"Загвар (λ={sim_lam})")
    ax1.set_title("Дарааллын уртын харьцуулалт")
    ax1.set_xlabel("Хугацаа (с)")
    ax1.set_ylabel("Машины тоо")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.hist(w_real, bins=30, alpha=0.5, color='blue', label=f"Бодит (λ={real_lam})")
    ax2.hist(w_sim, bins=30, alpha=0.5, color='orange', label=f"Загвар (λ={sim_lam})")
    ax2.set_title("Хүлээх хугацааны тархалтын харьцуулалт")
    ax2.set_xlabel("Хүлээх хугацаа (с)")
    ax2.set_ylabel("Машины тоо")
    ax2.grid(axis='y', alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}F.real_vs_sim_comparison.png')



def print_optimal_signal(lam, results, best_config, best_wait):
    print(f"\nλ = {lam} машин/мин үед гэрлэн дохионы оновчлолын үр дүн:")
    print("-" * 60)
    print(f"{'Ногоон (с)':<12} {'Улаан (с)':<12} {'Дундаж дараалал':<18} {'Дундаж хүлээлт (с)':<18}")
    print("-" * 60)
    avg_queues = []
    avg_waits = []
    for (green, red), (avg_q, avg_w) in results.items():
        print(f"{green:<12} {red:<12} {avg_q:<18.2f} {avg_w:<18.2f}")
        avg_queues.append(avg_q)
        avg_waits.append(avg_w)
    print("-" * 60)
    overall_q = np.mean(avg_queues)
    overall_w = np.mean(avg_waits)
    print(f"Нийт дундаж дараалал: {overall_q:.2f} машин")
    print(f"Нийт дундаж хүлээлт: {overall_w:.2f} секунд")
    print(f"Хамгийн бага хүлээлттэй тохиргоо: Ногоон {best_config[0]} с, Улаан {best_config[1]} с")
    print(f"Хамгийн бага дундаж хүлээлт: {best_wait:.2f} секунд\n")

def print_convergence_table(N_list, means, lows, highs, lam=15):
    print(f"\nМонте-Карло давталтын тогтворжилт (λ={lam}):")
    print("-" * 65)
    print(f"{'N':<10} {'Дундаж (сек)':<15} {'Доод хязгаар (95% CI)':<25} {'Дээд хязгаар (95% CI)':<25}")
    print("-" * 65)
    for i, N in enumerate(N_list):
        print(f"{N:<10} {means[i]:<15.4f} {lows[i]:<25.4f} {highs[i]:<25.4f}")
    print("-" * 65)

def print_comparison(real_lam=30, sim_lam=15, green=40, red=50, duration_sec=3600):
    """Бодит өгөгдөл ба загварын харьцуулалтыг терминалд хэвлэнэ."""
    stats = _compute_comparison_stats(real_lam, sim_lam, green, red, duration_sec)
    real = stats["real"]
    sim  = stats["sim"]

    print("\nБодит өгөгдөлтэй харьцуулалт (λ_бодит=30, λ_загвар=15):")
    print("-" * 65)
    print(f"{'Үзүүлэлт':<25} {'Бодит (λ=30)':<20} {'Загвар (λ=15)':<20}")
    print("-" * 65)
    print(f"{'Дундаж дараалал':<25} {real['queue']:<20.4f} {sim['queue']:<20.4f}")
    print(f"{'Дундаж хүлээлт (с)':<25} {real['wait']:<20.4f} {sim['wait']:<20.4f}")
    print(f"{'Нийт нэвтэрсэн машин':<25} {real['total']:<20} {sim['total']:<20}")
    print("-" * 65)


if __name__ == "__main__":
    plot_one_hour_direction_queue()
    plot_4_directions_queue()
    plot_24h_four_directions()
    plot_optimal_signal()
    plot_histogram_wait_times()
    plot_convergence_and_confidence()
    plot_comparison()

    plt.show()