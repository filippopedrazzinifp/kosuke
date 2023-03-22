import argparse
import logging
import time

from app import models, services

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Kosuke Code Assistant.")
parser.add_argument("--task", type=str, default="analyze")
parser.add_argument("--framework", type=str, default="django")
parser.add_argument("--question", type=str, default="Hello world!")
parser.add_argument("--since_date", type=str, default="2023-03-01")

args = parser.parse_args()


def main():
    if args.task == "analyze":
        services.generate_code_report(args.framework)
    elif args.task == "change_log":
        services.generate_change_log(args.since_date)
    elif args.task == "index_code_base":
        logger.info("Started job for indexing code base.")
        while True:
            services.index_code_base()
            time.sleep(60 * 60 * 3)  # 3h
    elif args.task == "init_pinecone":
        models.init_pinecone()
    elif args.task == "chat":
        response = services.generate_response(args.question)
        print(response)
    elif args.task == "code_review":
        logger.info("Started job for reviewing code.")
        while True:
            services.comment_pull_requests()
            time.sleep(60)  # 1m
    else:
        raise ValueError("Invalid task.")


main()
