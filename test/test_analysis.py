import numpy as np
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.analysis import calc_confidence_interval, find_optimal_signal


def test_calc_confidence_interval():
    data = [10, 12, 11, 13, 10, 14]
    mean, lower, upper = calc_confidence_interval(data)
    expected_mean = np.mean(data)
    expected_margin = 1.96 * np.std(data, ddof=1) / np.sqrt(len(data))
    assert mean == pytest.approx(expected_mean)
    assert lower == pytest.approx(expected_mean - expected_margin)
    assert upper == pytest.approx(expected_mean + expected_margin)


def test_calc_confidence_interval_single():
    mean, lower, upper = calc_confidence_interval([5])
    assert mean == 5
    assert lower == 5
    assert upper == 5


def test_find_optimal_signal():
    configs = [(30, 50), (40, 40), (50, 30)]
    best_config, best_wait, results = find_optimal_signal(lam=10, configs=configs, duration_sec=500)
    assert best_config in configs
    assert isinstance(best_wait, float)
    assert isinstance(results, dict)
    assert len(results) == len(configs)


def test_find_optimal_signal_high_load():
    configs = [(20, 60), (40, 40), (60, 20)]
    best_config, _, _ = find_optimal_signal(lam=30, configs=configs, duration_sec=500)
    assert best_config in configs