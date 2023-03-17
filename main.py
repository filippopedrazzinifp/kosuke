import argparse
import time

from app import services

parser = argparse.ArgumentParser(description="Kosuke Code Assistant.")
parser.add_argument("--task", type=str, default="code_review")
parser.add_argument("--framework", type=str, default="django")
parser.add_argument("--since_date", type=str, default="2023-03-01")

args = parser.parse_args()


def main():
    if args.task == "analyze":
        services.generate_code_report(args.framework)
    elif args.task == "change_log":
        services.generate_change_log(args.since_date)
    elif args.task == "code_review":
        while True:
            services.comment_merge_requests()
            time.sleep(60)
    else:
        raise ValueError("Invalid task.")


main()
