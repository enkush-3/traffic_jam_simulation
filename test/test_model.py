import numpy as np
import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.model import generate_arrivals, simulate_intersection

def test_generate_arrivals_shape():
    lam = 15
    duration = 100
    arrivals = generate_arrivals(lam, duration)
    assert arrivals.shape == (duration,)
    assert arrivals.dtype == int


def test_generate_arrivals_reproducible():
    rng = np.random.default_rng(42)
    a1 = generate_arrivals(15, 10, rng=rng)
    rng = np.random.default_rng(42)
    a2 = generate_arrivals(15, 10, rng=rng)
    np.testing.assert_array_equal(a1, a2)


def test_generate_arrivals_rate():
    lam = 10
    duration = 100000
    arrivals = generate_arrivals(lam, duration)
    mean_arrivals = np.mean(arrivals)
    assert abs(mean_arrivals - lam / 60.0) < 0.1


def test_simulate_intersection_basic():
    queue_log, wait_times = simulate_intersection(lam=5, green_sec=30, red_sec=30, duration_sec=100)
    assert len(queue_log) == 100
    assert all(q >= 0 for q in queue_log)
    assert all(w > 0 for w in wait_times) if wait_times else True


def test_simulate_intersection_no_traffic():
    queue_log, wait_times = simulate_intersection(lam=0, green_sec=40, red_sec=50, duration_sec=200)
    assert np.all(queue_log == 0)
    assert len(wait_times) == 0


def test_simulate_intersection_deterministic_seed():
    rng = np.random.default_rng(123)
    q1, w1 = simulate_intersection(lam=15, green_sec=40, red_sec=50, duration_sec=100, rng=rng)
    rng = np.random.default_rng(123)
    q2, w2 = simulate_intersection(lam=15, green_sec=40, red_sec=50, duration_sec=100, rng=rng)
    np.testing.assert_array_equal(q1, q2)
    np.testing.assert_array_equal(w1, w2)