import argparse
import pandas as pd
from . import DriftCheck

def main():
    parser = argparse.ArgumentParser(description="Watchdog Drift Checker")
    parser.add_argument("--ref", type=str, required=True, help="Reference dataset CSV")
    parser.add_argument("--cur", type=str, required=True, help="Current dataset CSV")
    parser.add_argument("--features", nargs="+", required=True, help="Feature columns to monitor")
    parser.add_argument("--algo", type=str, default="psi", help="Drift algorithm: psi or ks")
    parser.add_argument("--plot", action="store_true", help="Plot the drift")
    parser.add_argument("--out", type=str, help="Output JSON path")

    args = parser.parse_args()

    ref = pd.read_csv(args.ref)
    cur = pd.read_csv(args.cur)

    checker = DriftCheck(algorithm=args.algo)
    results = checker.run(ref, cur, args.features)

    for feat, result in results.items():
        print(result.summary())
        if args.plot:
            result.plot()
        if args.out:
            result.to_json(args.out)

if __name__ == "__main__":
    main()
