"""buildhub CLI.  Implement so:  python -m buildhub summarize <file> --group-by G --value V --agg A
and:  python -m buildhub top <file> --key K --n N   both work (see SPEC.md)."""
import argparse
import sys

from .datakit import load_records, summarize, to_report, top_n


def main(argv=None):
    parser = argparse.ArgumentParser(prog="buildhub")
    subparsers = parser.add_subparsers(dest="command", required=True)

    summarize_cmd = subparsers.add_parser("summarize")
    summarize_cmd.add_argument("file")
    summarize_cmd.add_argument("--group-by", required=True)
    summarize_cmd.add_argument("--value", required=True)
    summarize_cmd.add_argument("--agg", required=True)
    summarize_cmd.add_argument("--decimals", type=int, default=2)

    top_cmd = subparsers.add_parser("top")
    top_cmd.add_argument("file")
    top_cmd.add_argument("--key", required=True)
    top_cmd.add_argument("--n", type=int, required=True)

    args = parser.parse_args(argv)
    records = load_records(args.file)

    if args.command == "summarize":
        result = summarize(records, args.group_by, args.value, args.agg, args.decimals)
        print(to_report(result))
    elif args.command == "top":
        for row in top_n(records, args.key, args.n):
            print(row)

    return 0


if __name__ == "__main__":
    sys.exit(main())
