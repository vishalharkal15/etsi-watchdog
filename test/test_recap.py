# test/test_recap.py

import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from etsi.watchdog import DriftCheck, Monitor, recap_results, print_results_recap


def generate_test_data():
    """Generate test data with varying drift levels."""
    np.random.seed(42)
    ref = pd.DataFrame({
        'age': np.random.normal(30, 5, 500),
        'salary': np.random.normal(50000, 10000, 500),
        'score': np.random.normal(0.7, 0.1, 500)
    })

    # Create data with different drift levels
    live_normal = pd.DataFrame({
        'age': np.random.normal(31, 5, 500),      # Low drift
        'salary': np.random.normal(52000, 10000, 500),  # Low drift
        'score': np.random.normal(0.72, 0.1, 500)       # Low drift
    })
    
    live_drift = pd.DataFrame({
        'age': np.random.normal(40, 5, 500),      # High drift
        'salary': np.random.normal(80000, 15000, 500),  # High drift  
        'score': np.random.normal(0.5, 0.2, 500)        # Medium drift
    })
    
    return ref, live_normal, live_drift


def test_results_recap():
    """Test the recap_results utility function."""
    print("\n==== Testing recap_results() ====")
    ref, live_normal, live_drift = generate_test_data()
    
    # Test with normal data (low drift)
    check = DriftCheck(ref)
    results_normal = check.run(live_normal, features=["age", "salary", "score"])
    
    print("\n1. Testing with low drift data:")
    print_results_recap(results_normal)
    
    # Test with drifted data (high drift)
    results_drift = check.run(live_drift, features=["age", "salary", "score"])
    
    print("\n2. Testing with high drift data:")
    print_results_recap(results_drift)
    
    # Test programmatic access
    recap = recap_results(results_drift)
    assert "overview" in recap
    assert "statistics" in recap
    assert "feature_analysis" in recap
    assert "ranked_concerns" in recap
    
    print("\n[✓] recap_results() tests passed")


def test_monitor_recap():
    """Test the Monitor.recap() method."""
    print("\n==== Testing Monitor.recap() ====")
    ref, _, _ = generate_test_data()
    monitor = Monitor(ref)
    
    # Generate rolling data with increasing drift
    live_data = []
    for i in range(7):  # 7 days of data
        d = pd.DataFrame({
            'age': np.random.normal(30 + i * 2, 5, 100),  # Gradual drift
            'salary': np.random.normal(50000 + i * 5000, 10000, 100),  # Gradual drift
            'score': np.random.normal(0.7 - i * 0.05, 0.1, 100)  # Gradual drift
        })
        # Set datetime index
        start_date = datetime.today() - timedelta(days=6-i)
        d.index = pd.date_range(start=start_date, periods=100, freq="H")
        live_data.append(d)
    
    live_df = pd.concat(live_data)
    
    # Run rolling monitoring
    rolling_results = monitor.watch_rolling(
        live_df, 
        window=50, 
        freq="D", 
        features=["age", "salary", "score"]
    )
    
    # Test recap functionality
    print("\n1. Testing Monitor.print_recap():")
    monitor.print_recap(rolling_results)
    
    # Test programmatic access
    recap = monitor.recap(rolling_results)
    assert "monitoring_period" in recap
    assert "drift_summary" in recap
    assert "feature_analysis" in recap
    assert "top_concerns" in recap
    
    print("\n[✓] Monitor.recap() tests passed")


def test_empty_results():
    """Test recap functions with empty results."""
    print("\n==== Testing with empty results ====")
    
    # Test empty results dict
    print("1. Testing recap_results with empty dict:")
    print_results_recap({})
    
    # Test empty rolling results
    print("\n2. Testing Monitor.recap with empty list:")
    ref, _, _ = generate_test_data()
    monitor = Monitor(ref)
    monitor.print_recap([])
    
    print("\n[✓] Empty results tests passed")


if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    test_results_recap()
    test_monitor_recap() 
    test_empty_results()
    print("\n---All recap functionality tests passed----")