
import numpy as np
import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation import run_monte_carlo, get_lambda_for_hour, simulate_24h_one_direction, _compute_comparison_stats

def test_run_monte_carlo():
    mean_q, mean_w = run_monte_carlo(lam=15, green_sec=40, red_sec=50, duration_sec=100, n_trials=10)
    assert mean_q.shape == (10,)
    assert mean_w.shape == (10,)
    assert all(mq >= 0 for mq in mean_q)
    assert all(mw >= 0 for mw in mean_w)


def test_run_monte_carlo_reproducible():
    mean_q1, mean_w1 = run_monte_carlo(lam=5, n_trials=5, duration_sec=50)
    mean_q2, mean_w2 = run_monte_carlo(lam=5, n_trials=5, duration_sec=50)
    assert abs(np.mean(mean_q1) - np.mean(mean_q2)) < 2.0


def test_get_lambda_for_hour():
    assert get_lambda_for_hour(8) == 25.0 
    assert get_lambda_for_hour(9) == 25.0 
    assert get_lambda_for_hour(10) == 15.0
    assert get_lambda_for_hour(16) == 15.0
    assert get_lambda_for_hour(17) == 25.0
    assert get_lambda_for_hour(22) == 3.0 
    assert get_lambda_for_hour(2) == 3.0  
    assert get_lambda_for_hour(7) == 10.0 


def test_get_lambda_for_hour_boundary():
    assert get_lambda_for_hour(23) == 3.0
    assert get_lambda_for_hour(0) == 3.0
    assert get_lambda_for_hour(6) == 3.0
    assert get_lambda_for_hour(19) == 25.0


def test_simulate_24h_one_direction():
    mean_q, mean_w = simulate_24h_one_direction(green_sec=40, red_sec=50)
    assert mean_q.shape == (24,)
    assert mean_w.shape == (24,)
    assert all(mq >= 0 for mq in mean_q)
    assert all(mw >= 0 for mw in mean_w)


def test_simulate_24h_one_direction_different_cycles():
    mean_q1, mean_w1 = simulate_24h_one_direction(30, 60)
    mean_q2, mean_w2 = simulate_24h_one_direction(50, 30)
    assert not np.array_equal(mean_q1, mean_q2)


def test_compute_comparison_stats():
    stats = _compute_comparison_stats(real_lam=10, sim_lam=12, green=40, red=40, duration_sec=500)
    expected_keys = {"real", "sim", "q_real", "q_sim", "w_real", "w_sim"}
    assert set(stats.keys()) == expected_keys
    assert "queue" in stats["real"]
    assert "wait" in stats["sim"]
    assert len(stats["q_real"]) == 500
    assert len(stats["w_sim"]) >= 0


def test_compute_comparison_stats_consistency():
    lam = 15
    stats = _compute_comparison_stats(lam, lam, green=40, red=40, duration_sec=1000)
    assert abs(stats["real"]["queue"] - stats["sim"]["queue"]) < 2.0
    assert abs(stats["real"]["wait"] - stats["sim"]["wait"]) < 1.0