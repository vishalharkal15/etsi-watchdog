import argparse
import pandas as pd
from .drift.factory import DriftCheck
from .monitor import Monitor
from .compare import DriftComparator
from .logger import get_logger

logger = get_logger("cli")

def main():
    parser = argparse.ArgumentParser(description="Watchdog Drift Detection CLI")
    subparsers = parser.add_subparsers(dest="command")

    drift_cmd = subparsers.add_parser("drift")
    drift_cmd.add_argument("--ref", required=True)
    drift_cmd.add_argument("--live", required=True)
    drift_cmd.add_argument("--algo", default="ks")
    drift_cmd.add_argument("--threshold", type=float, default=0.1)

    monitor_cmd = subparsers.add_parser("monitor")
    monitor_cmd.add_argument("--ref", required=True)
    monitor_cmd.add_argument("--live", required=True)
    monitor_cmd.add_argument("--interval", type=int, default=60)
    monitor_cmd.add_argument("--algo", default="ks")

    compare_cmd = subparsers.add_parser("compare")
    compare_cmd.add_argument("--v1", required=True)
    compare_cmd.add_argument("--v2", required=True)

    args = parser.parse_args()

    if args.command == "drift":
        ref = pd.read_csv(args.ref)
        live = pd.read_csv(args.live)
        checker = DriftCheck(algo=args.algo, threshold=args.threshold)
        result = checker.run(ref, live)
        print(result)

    elif args.command == "monitor":
        mon = Monitor(interval_sec=args.interval, algo=args.algo)
        mon.run(args.ref, args.live)

    elif args.command == "compare":
        comp = DriftComparator(args.v1, args.v2)
        print(comp.compare())

if __name__ == "__main__":
    main()
