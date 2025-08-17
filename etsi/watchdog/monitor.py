# etsi/watchdog/monitor.py

from .drift_check import DriftCheck
from .logger import log_drift
import pandas as pd


class Monitor:
    """
    Monitor — Periodic/rolling drift monitoring.

    Example:
    >>> monitor = Monitor(reference_df)
    >>> monitor.enable_logging("logs/drift.csv")
    >>> monitor.watch(live_df)
    """

    def __init__(self, reference_df):
        self.reference = reference_df
        self.log_path = None

    def enable_logging(self, path: str):
        self.log_path = path

    def watch(self, live_df: pd.DataFrame, features=None, algorithm="psi", threshold=0.2):
        checker = DriftCheck(self.reference, algorithm=algorithm, threshold=threshold)
        features = features or list(self.reference.columns)
        results = checker.run(live_df, features=features)

        for feat, res in results.items():
            if self.log_path:
                log_drift(res, self.log_path, feature=feat)
        return results

    def watch_rolling(self, live_df: pd.DataFrame, window=50, freq="D", features=None, algorithm="psi", threshold=0.2):
        if not isinstance(live_df.index, pd.DatetimeIndex):
            raise ValueError("Live data must have a DatetimeIndex for rolling drift detection.")

        results = []
        for timestamp, group in live_df.groupby(pd.Grouper(freq=freq)):
            if len(group) >= window:
                chunk = group.tail(window)
                result = self.watch(chunk, features=features, algorithm=algorithm, threshold=threshold)
                results.append((timestamp, result))
        return results

    def recap(self, rolling_results):
        """
        Generate a comprehensive recap summary of rolling drift monitoring results.
        
        Args:
            rolling_results: List of (timestamp, results_dict) tuples from watch_rolling()
            
        Returns:
            dict: Comprehensive recap with drift statistics and insights
        """
        if not rolling_results:
            return {"message": "No rolling results to recap"}
        
        # Extract all features and periods
        all_features = set()
        periods_data = []
        
        for timestamp, results in rolling_results:
            period_data = {"timestamp": timestamp}
            for feature, drift_result in results.items():
                all_features.add(feature)
                period_data[f"{feature}_score"] = drift_result.score
                period_data[f"{feature}_drifted"] = drift_result.is_drifted
            periods_data.append(period_data)
        
        # Calculate feature-wise statistics
        feature_stats = {}
        for feature in all_features:
            scores = [p[f"{feature}_score"] for p in periods_data if f"{feature}_score" in p]
            drifted_flags = [p[f"{feature}_drifted"] for p in periods_data if f"{feature}_drifted" in p]
            
            if scores:
                feature_stats[feature] = {
                    "total_periods": len(scores),
                    "drift_periods": sum(drifted_flags),
                    "drift_rate": sum(drifted_flags) / len(drifted_flags) if drifted_flags else 0,
                    "avg_score": sum(scores) / len(scores),
                    "max_score": max(scores),
                    "min_score": min(scores),
                    "latest_score": scores[-1] if scores else None,
                    "trending": "up" if len(scores) >= 2 and scores[-1] > scores[-2] else "down" if len(scores) >= 2 else "stable"
                }
        
        # Overall summary
        total_periods = len(rolling_results)
        total_drift_events = 0
        
        # Count total drift events across all periods and features
        for timestamp, results in rolling_results:
            for feature, drift_result in results.items():
                if drift_result.is_drifted:
                    total_drift_events += 1
        
        overall_drift_rate = total_drift_events / (total_periods * len(all_features)) if total_periods and all_features else 0
        
        # Most problematic features
        worst_features = sorted(feature_stats.items(), 
                               key=lambda x: (x[1]["drift_rate"], x[1]["max_score"]), 
                               reverse=True)
        
        recap_summary = {
            "monitoring_period": {
                "total_periods": total_periods,
                "date_range": f"{rolling_results[0][0].date()} to {rolling_results[-1][0].date()}" if rolling_results else "N/A",
                "features_monitored": list(all_features)
            },
            "drift_summary": {
                "overall_drift_rate": round(overall_drift_rate, 4),
                "total_drift_events": total_drift_events,
                "health_status": "healthy" if overall_drift_rate < 0.2 else "warning" if overall_drift_rate < 0.5 else "critical"
            },
            "feature_analysis": feature_stats,
            "top_concerns": [{"feature": feat, **stats} for feat, stats in worst_features[:3]]
        }
        
        return recap_summary
    
    def print_recap(self, rolling_results):
        """Print a formatted recap summary to console."""
        recap = self.recap(rolling_results)
        
        if "message" in recap:
            print(f"[etsi-watchdog] {recap['message']}")
            return
            
        print("\n" + "="*60)
        print(" "*20 + "DRIFT MONITORING RECAP")
        print("="*60)
        
        # Monitoring period
        period = recap["monitoring_period"]
        print(f"📅 Monitoring Period: {period['date_range']}")
        print(f"📊 Total Periods: {period['total_periods']}")
        print(f"🎯 Features Monitored: {', '.join(period['features_monitored'])}")
        
        # Overall health
        drift_info = recap["drift_summary"]
        health_emoji = {"healthy": "✅", "warning": "⚠️", "critical": "🚨"}
        health_status = drift_info["health_status"]
        print(f"\n{health_emoji.get(health_status, '❓')} Overall Health: {health_status.upper()}")
        print(f"📈 Drift Rate: {drift_info['overall_drift_rate']:.1%}")
        print(f"🚩 Total Drift Events: {drift_info['total_drift_events']}")
        
        # Top concerns
        if recap["top_concerns"]:
            print(f"\n🔍 TOP CONCERNS:")
            for i, concern in enumerate(recap["top_concerns"], 1):
                trend_emoji = {"up": "📈", "down": "📉", "stable": "➡️"}
                print(f"  {i}. {concern['feature']}: {concern['drift_rate']:.1%} drift rate "
                      f"(max: {concern['max_score']:.3f}) {trend_emoji.get(concern['trending'], '')}")
        
        print("="*60)
