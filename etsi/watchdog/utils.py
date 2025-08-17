import pandas as pd
from datetime import datetime
from pathlib import Path
import json
import warnings

def log_drift_result(psi_scores, drift_status, path: str):
    """
    Appends drift results (timestamp + PSI scores) to a CSV or JSON log file.
    """
    # Type safety
    if not isinstance(psi_scores, dict):
        raise TypeError("psi_scores must be a dict")

    timestamp = datetime.now().isoformat()
    row = {
        "timestamp": timestamp,
        "drift": drift_status,
        **psi_scores
    }

    path_obj = Path(path)
    path_obj.parent.mkdir(parents=True, exist_ok=True)

    # CSV logging
    if path_obj.suffix == ".csv":
        df = pd.DataFrame([row])
        if not path_obj.exists():
            df.to_csv(path_obj, index=False)
        else:
            df.to_csv(path_obj, mode='a', header=False, index=False)
        print(f"[etsi-watchdog] Logged drift event to {path_obj.resolve()}")

    # JSON logging (append style)
    elif path_obj.suffix == ".json":
        if path_obj.exists():
            try:
                existing = json.loads(path_obj.read_text())
                if not isinstance(existing, list):
                    existing = []
            except json.JSONDecodeError:
                existing = []
        else:
            existing = []

        existing.append(row)
        path_obj.write_text(json.dumps(existing, indent=2))
        print(f"[etsi-watchdog] Logged drift event to {path_obj.resolve()}")

    else:
        warnings.warn(f"[etsi-watchdog] Unsupported log format: {path_obj.suffix}. Use .csv or .json")


def recap_results(results_dict):
    """
    Generate a comprehensive recap summary from a dictionary of DriftResult objects.
    
    Args:
        results_dict: Dictionary with feature names as keys and DriftResult objects as values
        
    Returns:
        dict: Comprehensive recap with feature-wise analysis and overall statistics
    """
    if not results_dict:
        return {"message": "No drift results to recap"}
    
    # Feature-wise analysis
    feature_analysis = {}
    scores = []
    drift_count = 0
    
    for feature, result in results_dict.items():
        feature_analysis[feature] = {
            "method": result.method,
            "score": result.score,
            "threshold": result.threshold,
            "is_drifted": result.is_drifted,
            "sample_size": result.sample_size,
            "drift_severity": "high" if result.score > result.threshold * 2 else "medium" if result.is_drifted else "low"
        }
        scores.append(result.score)
        if result.is_drifted:
            drift_count += 1
    
    # Overall statistics
    total_features = len(results_dict)
    avg_score = sum(scores) / len(scores) if scores else 0
    max_score = max(scores) if scores else 0
    drift_rate = drift_count / total_features if total_features > 0 else 0
    
    # Rank features by drift severity
    ranked_features = sorted(feature_analysis.items(), 
                           key=lambda x: (x[1]["is_drifted"], x[1]["score"]), 
                           reverse=True)
    
    # Overall health assessment
    health_status = "healthy"
    if drift_rate > 0.5:
        health_status = "critical"
    elif drift_rate > 0.2 or max_score > 1.0:
        health_status = "warning"
    
    recap_summary = {
        "overview": {
            "total_features": total_features,
            "features_with_drift": drift_count,
            "drift_rate": round(drift_rate, 4),
            "health_status": health_status
        },
        "statistics": {
            "avg_score": round(avg_score, 4),
            "max_score": round(max_score, 4),
            "min_score": round(min(scores), 4) if scores else 0
        },
        "feature_analysis": feature_analysis,
        "ranked_concerns": [{"feature": feat, **stats} for feat, stats in ranked_features]
    }
    
    return recap_summary


def print_results_recap(results_dict):
    """Print a formatted recap of DriftResult objects to console."""
    recap = recap_results(results_dict)
    
    if "message" in recap:
        print(f"[etsi-watchdog] {recap['message']}")
        return
    
    print("\n" + "="*50)
    print(" "*15 + "DRIFT ANALYSIS RECAP")
    print("="*50)
    
    # Overview
    overview = recap["overview"]
    health_emoji = {"healthy": "✅", "warning": "⚠️", "critical": "🚨"}
    health_status = overview["health_status"]
    
    print(f"🎯 Features Analyzed: {overview['total_features']}")
    print(f"🚩 Features with Drift: {overview['features_with_drift']}")
    print(f"📊 Drift Rate: {overview['drift_rate']:.1%}")
    print(f"{health_emoji.get(health_status, '❓')} Health Status: {health_status.upper()}")
    
    # Statistics
    stats = recap["statistics"]
    print(f"\n📈 Score Statistics:")
    print(f"   Average: {stats['avg_score']:.4f}")
    print(f"   Maximum: {stats['max_score']:.4f}")
    print(f"   Minimum: {stats['min_score']:.4f}")
    
    # Top concerns
    concerns = recap["ranked_concerns"]
    drifted_concerns = [c for c in concerns if c["is_drifted"]]
    
    if drifted_concerns:
        print(f"\n🔍 FEATURES REQUIRING ATTENTION:")
        for i, concern in enumerate(drifted_concerns[:5], 1):
            severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
            severity = concern["drift_severity"]
            print(f"  {i}. {concern['feature']}: {concern['score']:.4f} "
                  f"{severity_emoji.get(severity, '')} ({severity} severity)")
    else:
        print(f"\n✅ All features are within acceptable drift thresholds!")
    
    print("="*50)
