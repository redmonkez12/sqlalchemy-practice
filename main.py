import argparse

from db import db_connect, create_tables, create_tables_orm
from task_mapper import task_mapper


def run():
    parser = argparse.ArgumentParser(description="Select a task and a type")
    parser.add_argument("--task")
    parser.add_argument("--type")
    args = parser.parse_args()

    if not args.task:
        raise Exception("Select task you want to run")

    if not args.type:
        raise Exception("Select if you want to run orm or core")

    engine = db_connect()

    if args.task in task_mapper and args.type in task_mapper[args.task]:
        task_function = task_mapper[args.task][args.type]

        def create_tables_callback():
            if args.type == "orm":
                create_tables_orm(engine)
            elif args.type == "core":
                create_tables(engine)

        task_function(engine, create_tables_callback)
    else:
        raise Exception("Invalid task or type selected")


if __name__ == "__main__":
    run()
